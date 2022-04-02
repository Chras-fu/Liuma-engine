class WebOperationCollection:

    def __init__(self):
        self.id = None
        self.opt_type = None
        self.opt_name = None
        self.opt_trans = None
        self.opt_element = None
        self.opt_data = None
        self.opt_code = None

    @staticmethod
    def __parse(ui_data: dict, name):
        if name not in ui_data:
            return None
        return ui_data.get(name)

    def collect_id(self, ui_data):
        self.id = WebOperationCollection.__parse(ui_data, "operationId")

    def collect_opt_type(self, ui_data):
        self.opt_type = WebOperationCollection.__parse(ui_data, "operationType")

    def collect_opt_name(self, ui_data):
        self.opt_name = WebOperationCollection.__parse(ui_data, "operationName")

    def collect_opt_trans(self, ui_data):
        self.opt_trans = WebOperationCollection.__parse(ui_data, "operationTrans")

    def collect_opt_code(self, ui_data):
        self.opt_code = WebOperationCollection.__parse(ui_data, "operationCode")

    def collect_opt_element(self, ui_data):
        opt_element = WebOperationCollection.__parse(ui_data, "operationElement")
        if opt_element is None or len(opt_element) == 0:
            self.opt_element = None
        else:
            for element in opt_element.values():
                element.pop("target")
            self.opt_element = opt_element

    def collect_opt_data(self, ui_data):
        opt_data = WebOperationCollection.__parse(ui_data, "operationData")
        if opt_data is None or len(opt_data) == 0:
            self.opt_data = None
        else:
            self.opt_data = opt_data

    def collect(self, ui_data):
        self.collect_id(ui_data)
        self.collect_opt_type(ui_data)
        self.collect_opt_name(ui_data)
        self.collect_opt_trans(ui_data)
        self.collect_opt_element(ui_data)
        self.collect_opt_data(ui_data)
        self.collect_opt_code(ui_data)
