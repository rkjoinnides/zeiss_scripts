import input_validation
import sys


class Menu:

    def __init__(self, is_submenu: bool = False, parent_menu=None):

        self.items = []

        #   submenus do not get exit option
        if is_submenu:
            self.has_exit = True
            self.parent_menu = parent_menu

            #   add_option for menu elevations
            self.items.append(Item("Go Back",
                              item_action=parent_menu.choose_item))

        else:
            self.has_exit = False

    def show(self) -> None:
        for idx, item in enumerate(self.items):

            string_to_print = item.name
            if item.is_dependant and not item.master_option.selected:
                string_to_print += "(locked)"

            #   shift options by 1 for display
            print("{}) {}".format(idx + 1, string_to_print))

    def add_item(self, option_name, **kwargs) -> None:
        # option_name: str, option_action: Callable = None,
        # option_args: List = None, dependant_option: str = None

        item_action = assign_keyword_arg("item_action", kwargs)
        item_args = assign_keyword_arg("item_args", kwargs)
        dependant_option = assign_keyword_arg("item_option", kwargs)
        use_dependent_result = assign_keyword_arg("use_dependent_result",
                                                  kwargs)

        #   Add dependent option if specified
        if dependant_option is not None:
            dependant_option = self.items[self.find_index(dependant_option)]

            #   Link dependent item's args to master's result
            if use_dependent_result is not None:
                item_args = dependant_option.result

        item = Item(option_name, item_action=item_action,
                    item_arguments=item_args, master_item=dependant_option,
                    use_master_result=use_dependent_result)

        #   Maintain exit as last item in menu
        insertion_idx = len(self.items)
        if not self.has_exit:
            self.add_exit()
        else:
            insertion_idx -= 1

        self.items.insert(insertion_idx, item)

    def add_sub_menu(self, submenu_name: str, submenu):
        sub = Item(submenu_name, item_action=submenu.choose_item)
        self.items.insert(len(self.items) - 1, sub)

    def choose_item(self):
        print("Please choose an item")
        response = ""
        while response != len(self.items) - 1:

            self.show()

            # shift responses by 1 for display
            response = input_validation.validate_int(1, len(self.items)) - 1
            selected_option = self.items[response]

            #   If the option is dependant on another
            if selected_option.is_dependant:

                #   Check if the master option has been selected
                if selected_option.master_option.selected:
                    selected_option.perform_action()
                else:
                    print("Please execute {} first".format(
                          selected_option.master_option.name))

            else:
                selected_option.perform_action()

    def add_exit(self):
        self.items.append(Item("Exit", item_action=menu_exit))
        self.has_exit = True

    def find_index(self, input_option_name: str):
        for idx, option in enumerate(self.items):
            if option.name == input_option_name:
                return idx


class Item:

    def __init__(self, item_name: str, **kwargs):
        # item_action: Callable[..., None], item_action_args: List = None

        self.name = item_name

        self.action = assign_keyword_arg("item_action", kwargs)
        self.args = assign_keyword_arg("item_arguments", kwargs)

        self.master_option = assign_keyword_arg("master_item", kwargs)
        self.use_master_results = assign_keyword_arg("use_master_result",
                                                     kwargs)

        self.is_dependant = False

        if self.master_option is not None:
            self.is_dependant = True

        if self.use_master_results is not None:
            self.args = self.master_option.result

        self.selected = False

        self.result = None

    def perform_action(self):

        #   case for fcn with no args and no dependant
        if self.args is None and not self.is_dependant:
            self.result = self.action()

        #   otherwise update the results
        else:
            if self.use_master_results is not None:
                self.update_args()
            self.result = self.action(*self.args)

        self.selected = True

    def set_dependence(self):
        self.is_dependant = True
        self.args = self.master_option.result

    def update_args(self):
        self.args = self.master_option.result


def assign_keyword_arg(arg_name, keyword_args):
    arg_to_return = None
    if arg_name in keyword_args:
        arg_to_return = keyword_args[arg_name]
    return arg_to_return


def printer(x):
    print(x)
    return (x)


def ind_print():
    print("Hello")


def menu_exit():
    input("Press enter to exit\n")
    sys.exit(0)


if __name__ == "__main__":

    M = Menu()

    M.add_item("Print x", item_action=printer, item_args=["x"])
    M.add_item("Print x dependent", item_action=printer, item_option="Print x",
               item_args=["aaa"])
    M.add_item("Say Hello", item_action=ind_print)

    M2 = Menu(is_submenu=True, parent_menu=M)
    M2.add_item("Hello", item_action=ind_print)
    M.add_sub_menu("Submenu 1", M2)

    M.choose_item()
