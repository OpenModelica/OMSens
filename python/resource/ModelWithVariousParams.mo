model ModelWithVariousParams
  // Params
  parameter Real    realParam1 = 1.121;
  parameter Real    realParam2 = 1.122;
  parameter Real    realParam3 = 1.123;
  parameter Integer intParam1  = 101;
  parameter Integer intParam2  = 102;
  parameter Integer intParam3  = 103;

  // Vars
  output Real outvar1;
  output Real outvar2;
  output Real outvar3;
equation
  outvar1 = time * realParam1 * intParam1;
  outvar2 = time * realParam2 * intParam2;
  outvar3 = time * realParam3 * intParam3;
end ModelWithVariousParams;
