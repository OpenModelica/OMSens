project(OMSens)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        DESTINATION share/OMSens
        PATTERN ".git/" EXCLUDE
        PATTERN ".jenkins/" EXCLUDE)
