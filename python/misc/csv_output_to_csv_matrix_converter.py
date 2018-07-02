import csv
import re  # regex
import logging  # en reemplazo de los prints

logger = logging.getLogger("--CSV output to CSV Matrix converter--")  # un logger especifico para este modulo

# Mine
import filesystem.files_aux


def W3TheoSensCSVToMatrixCSVFromYear(w3theosens_csv_file_path, output_matrix_path, year):
    # As we only use 2 rows of the whole file, it would be smarter to just get those lines instead of the whole file.
    # TO DO: read only the 2 needed lines instead of the whole file

    # Read the file into memory
    w3TheoSens_str = filesystem.files_aux.readStrFromFile(w3theosens_csv_file_path)
    # Process the string
    rows_str_list = W3TheoSensToMatrixRowsListFromYear(w3TheoSens_str, year)
    output_matrix_str = "\n".join(rows_str_list)
    # Write the resulting matrix to file
    filesystem.files_aux.writeStrToFile(output_matrix_str, output_matrix_path)


def W3TheoSensToMatrixRowsListFromYear(w3theosens_csv_str, year):
    str_lines_list = w3theosens_csv_str.split("\n")
    w3theosens_header_row = str_lines_list[0]
    w3theosens_year_row = None
    for row_str in str_lines_list:
        year_str = str(year)
        # Assuming that the year is first in the column (the variable Time is the first variable in OpenModelica outputs)
        first_chars_from_row_str = row_str[0:len(year_str)]
        if first_chars_from_row_str == year_str:
            w3theosens_year_row = row_str
            break

    if not w3theosens_year_row:
        raise InvalidYearException("The year " + str(year) + " has no associated row in the file")
    rows_str_list = W3TheoSensToMatrixRowsListFromHeadersAndYearRow(w3theosens_header_row, w3theosens_year_row)
    return rows_str_list


def W3TheoSensToMatrixRowsListFromHeadersAndYearRow(header_row, year_row):
    # For each "$Sensitivities.param.var" in header_row get its value for the year in year_row
    header_row_list = header_row.split(",")
    year_row_list = year_row.split(",")
    if (len(header_row_list) != len(year_row_list)):
        raise InvalidW3TheoSensCSVException("There are " + str(len(header_row_list)) + " 'sens-variables' and " + str(
            len(year_row_list)) + " values. The amount should be equal.")
    param_influences_dict = {}  # dict that will be filled with {"param_1":{"var_1":43,"var_2",41},...}
    # Iterate variables
    for i in range(0, len(header_row_list)):
        # Check if its a sensitivity param/variable value
        complex_var_name = header_row_list[i]
        # Check if its a sens param/variable value
        w3TheoSens_regex = "\$Sensitivities\..*"
        if re.match(w3TheoSens_regex, complex_var_name):
            param_name, var_name = extractParamNameAndVarNameFromComplexVarName(complex_var_name)
            # Add parameter influence to variable to the param_influences_dict dict
            # Try to get the "influenced_vars_by_param" dict for the param
            if param_name in param_influences_dict:
                influenced_vars_by_param = param_influences_dict[param_name]
            # If the key for this param hasn't been initialized yet, initialize it
            else:
                param_influences_dict[param_name] = {}
                influenced_vars_by_param = param_influences_dict[param_name]
            # Check if the variable sensitivity to his param has already been set
            if var_name in influenced_vars_by_param:
                # Raise exception because this means that we have 2 sensitivities of a variable to the same param (invalid data)
                raise RepeatedParamVarPairException(
                    "The parameter " + param_name + " has 2 influences to variable " + var_name + ".")
            else:
                # Get the value for this "param/var" pair from the year_row_list
                param_influence_to_variable = year_row_list[i]

                # Set the variable sensitivity to this param
                influenced_vars_by_param[var_name] = param_influence_to_variable

    rows_str_list = fromParamInfluencesDictToRowsStrList(param_influences_dict)
    return rows_str_list


def fromParamInfluencesDictToRowsStrList(param_influences_dict):
    matrix_str = ""
    # Set variables (column) order from vars_dict from any param
    # Get variables influenced dict from any param
    some_param_name, influenced_vars_by_some_param = next(iter(param_influences_dict.items()))
    vars_columns_order = list(influenced_vars_by_some_param.keys())

    first_row_str = "param\\var," + ",".join(vars_columns_order)
    rows_str_list = [first_row_str]
    # Iterate parameters in dict
    for param_name in param_influences_dict:
        influenced_vars_by_param = param_influences_dict[param_name]
        # Check that the amount of vars influenced by this param is the same as the "default" to prevent that this dict has more variables than the default
        if len(influenced_vars_by_param.keys()) != len(vars_columns_order):
            # Raise exception because this means that 2 params influence different variables
            raise DifferentInfluencedVariablesException(
                "The parameter " + param_name + " has differen influenced variables than param " + some_param_name + ".")
        # Iterate variables in order:
        row_str = param_name
        for var_name in vars_columns_order:
            row_str = row_str + "," + str(influenced_vars_by_param[var_name])
        rows_str_list.append(row_str)
    return rows_str_list


def extractParamNameAndVarNameFromComplexVarName(complex_var_name):
    # Parse the variable name and extract the parameter and "real" variable (the "real" variable may contain more than one dot ".")
    # Remove the "$Sensitivities." part
    param_var_dot_separated_str = complex_var_name.split("$Sensitivities.")[1]
    # Split into list the parameter and variable by dots
    param_var_dot_separated_list = param_var_dot_separated_str.split(".")
    # Extract the parameter name
    param_name = param_var_dot_separated_list[0]
    # Extract the variable name from the remaining positions in the list (>1 if more than one dot "." in its name)
    var_name = ".".join(param_var_dot_separated_list[1:])  # from the second position to the end
    return param_name, var_name


# Exception classes:
class InvalidW3TheoSensCSVException(Exception):
    pass


class RepeatedParamVarPairException(Exception):
    pass


class DifferentInfluencedVariablesException(Exception):
    pass


class InvalidYearException(Exception):
    pass
