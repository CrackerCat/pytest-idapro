import sys
import types


# TODO: unite a single list in a single location. perhaps just proxy every
# module that starts with ida_
modules_list = ['ida_allins', 'ida_area', 'ida_auto', 'ida_bytes', 'ida_dbg',
                'ida_diskio', 'ida_entry', 'ida_enum', 'ida_expr', 'ida_fixup',
                'ida_fpro', 'ida_frame', 'ida_funcs', 'ida_gdl', 'ida_graph',
                'ida_hexrays', 'ida_ida', 'ida_idaapi', 'ida_idd', 'ida_idp',
                'ida_ints', 'ida_kernwin', 'ida_lines', 'ida_loader',
                'ida_moves', 'ida_nalt', 'ida_name', 'ida_netnode',
                'ida_offset', 'ida_pro', 'ida_queue', 'ida_registry',
                'ida_search', 'ida_segment', 'ida_srarea', 'ida_strlist',
                'ida_struct', 'ida_typeinf', 'ida_ua', 'ida_xref']
modules_list.extend(['idaapi', 'idc', 'idautils'])


class ProxyModuleLoader(object):
    def __init__(self):
        self.loading = set()

    def find_module(self, fullname, path):
        print("module searched", fullname, path)
        if fullname in self.loading:
            return None
        if fullname in modules_list:
            print("module matched", fullname)
            return self

    def load_module(self, fullname):
        # for reload to function properly, must return existing instance if one
        # exists
        if fullname in sys.modules:
            return sys.modules[fullname]

        # otherwise, we'll create a module mockup
        # lock itself from continuously claiming to find ida modules, so that
        # the call to __import__ will not reach here again causing an infinite
        # recursion
        self.loading.add(fullname)
        real_module = __import__(fullname, None, None, "*")
        self.loading.remove(fullname)

        module = sys.modules[fullname] = ProxyModule(fullname, real_module)
        return module


class ProxyModule(types.ModuleType):
    def __init__(self, fullname, module):
        super(ProxyModule, self).__init__(fullname)
        self.__module = module
        print(self.__module)

    def __getattr__(self, name):
        return getattr(self.__module, name)

    def __setattr__(self, name, value):
        # TODO: implement set attr proxy
        pass


sys.meta_path.insert(0, ProxyModuleLoader())
