def validate_int(min_int=None, max_int=None):

    is_valid = False

    message = ""
    test_int = 0

    while not is_valid:

        is_int = True
        print(message, end="")
        x = input()

        try:
            test_int = int(x)
        except ValueError:
            is_int = False
            message = "Enter an integer \n"

        if is_int:

            #   case for only a min
            if min_int is not None and max_int is None:
                if test_int >= min_int:
                    is_valid = True
                else:
                    message = "Enter an integer greater than {}\n".format(min_int)

            #   case for only a max bound
            elif max_int is not None and min_int is None:
                if test_int <= max_int:
                    is_valid = True
                else:
                    message = "Enter an integer less than {}\n".format(max_int)

            #   case for both max and min supplied
            else:
                if (test_int >= min_int) and (test_int <= max_int):
                    is_valid = True
                else:
                    message = "Enter an integer between {} and {}\n".format(min_int, max_int)

    return test_int
