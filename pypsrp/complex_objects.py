# Copyright: (c) 2018, Jordan Borean (@jborean93) <jborean93@gmail.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from copy import deepcopy


class ObjectMeta(object):

    def __init__(self, tag="*", name=None, optional=False, object=None):
        self.tag = tag
        self.name = name
        self.optional = optional
        self.object = object


class ListMeta(ObjectMeta):

    def __init__(self, obj_type="LST", name=None, optional=False,
                 list_value_meta=None, list_types=None):
        super(ListMeta, self).__init__(obj_type, name, optional)

        if list_value_meta is None:
            self.list_value_meta = ObjectMeta()
        else:
            self.list_value_meta = list_value_meta

        if list_types is None:
            self.list_types = [
                "System.Object[]",
                "System.Array",
                "System.Object"
            ]
        else:
            self.list_types = list_types


class StackMeta(ListMeta):

    def __init__(self, name=None, optional=False, list_value_meta=None,
                 list_types=None):
        if list_types is None:
            list_types = [
                "System.Collections.Stack",
                "System.Object"
            ]
        super(StackMeta, self).__init__("STK", name, optional, list_value_meta,
                                        list_types)


class QueueMeta(ListMeta):
    def __init__(self, name=None, optional=False, list_value_meta=None,
                 list_types=None):
        if list_types is None:
            list_types = [
                "System.Collections.Queue",
                "System.Object"
            ]
        super(QueueMeta, self).__init__("QUE", name, optional, list_value_meta,
                                        list_types)


class DictionaryMeta(ObjectMeta):

    def __init__(self, name=None, optional=False, dict_key_meta=None,
                 dict_value_meta=None, dict_types=None):
        super(DictionaryMeta, self).__init__("DCT", name, optional)
        if dict_key_meta is None:
            self.dict_key_meta = ObjectMeta(name="Key")
        else:
            self.dict_key_meta = dict_key_meta

        if dict_value_meta is None:
            self.dict_value_meta = ObjectMeta(name="Value")
        else:
            self.dict_value_meta = dict_value_meta

        if dict_types is None:
            self.dict_types = [
                "System.Collections.Hashtable",
                "System.Object"
            ]
        else:
            self.dict_types = dict_types


class ComplexObject(object):

    def __init__(self):
        self._adapted_properties = ()
        self._extended_properties = ()
        self._property_sets = ()
        self._types = []
        self._to_string = None
        self._xml = None  # only populated on deserialization

    def __str__(self):
        return self._to_string


class GenericComplexObject(ComplexObject):

    def __init__(self):
        super(GenericComplexObject, self).__init__()
        self.property_sets = []
        self.extended_properties = {}
        self.adapted_properties = {}
        self.to_string = None
        self.types = []

    def __str__(self):
        return self.to_string


class Enum(ComplexObject):

    def __init__(self, enum_type, string_map, **kwargs):
        super(Enum, self).__init__()
        self._types = [
            "System.Enum",
            "System.ValueType",
            "System.Object"
        ]
        if enum_type is not None:
            self._types.insert(0, enum_type)

        self._property_sets = (
            ('value', ObjectMeta("I32")),
        )
        self._string_map = string_map

        self.value = kwargs.get('value')

    @property
    def _to_string(self):
        try:
            return self._string_map[self.value]
        except KeyError as err:
            raise KeyError("%s is not a valid enum value for %s, valid values "
                           "are %s" % (err, self._types[0], self._string_map))

    @_to_string.setter
    def _to_string(self, value):
        pass


# PSRP Complex Objects - https://msdn.microsoft.com/en-us/library/dd302883.aspx
class Coordinates(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.1 Coordinates
        https://msdn.microsoft.com/en-us/library/dd302883.aspx

        :param x: The X coordinate (0 is the leftmost column)
        :param y: The Y coordinate (0 is the topmsot row)
        """
        super(Coordinates, self).__init__()
        self._extended_properties = (
            ('_type', ObjectMeta("S", name="T")),
            ('_value', ObjectMeta("ObjDynamic", name="V",
                                  object=GenericComplexObject)),
        )
        self._type = "System.Management.Automation.Host.Coordinates"
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')

    @property
    def _value(self):
        gen_object = GenericComplexObject()
        gen_object.extended_properties['x'] = self.x
        gen_object.extended_properties['y'] = self.y
        return gen_object

    @_value.setter
    def _value(self, value):
        self.x = value.extended_properties['x']
        self.y = value.extended_properties['y']


class Size(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.2 Size
        https://msdn.microsoft.com/en-us/library/dd305083.aspx

        :param width: The width of the size
        :param height: The height of the size
        """
        super(Size, self).__init__()
        self._extended_properties = (
            ('_type', ObjectMeta("S", name="T")),
            ('_value', ObjectMeta("ObjDynamic", name="V",
                                  object=GenericComplexObject)),
        )
        self._type = "System.Management.Automation.Host.Size"
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')

    @property
    def _value(self):
        gen_object = GenericComplexObject()
        gen_object.extended_properties['width'] = self.width
        gen_object.extended_properties['height'] = self.height
        return gen_object

    @_value.setter
    def _value(self, value):
        self.width = value.extended_properties['width']
        self.height = value.extended_properties['height']


class Color(ComplexObject):
    DARK_BLUE = 1
    DARK_GREEN = 2
    DARK_CYAN = 3
    DARK_RED = 4
    DARK_MAGENTA = 5
    DARK_YELLOW = 6
    GRAY = 7
    DARK_GRAY = 8
    BLUE = 9
    GREEN = 10
    CYAN = 11
    RED = 12
    MAGENTA = 13
    YELLOW = 14
    WHITE = 15

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.3 Color
        https://msdn.microsoft.com/en-us/library/dd360026.aspx

        :param color The color int value to set
        """
        super(Color, self).__init__()
        self._extended_properties = (
            ('_type', ObjectMeta("S", name="T")),
            ('color', ObjectMeta("I32", name="V")),
        )
        self._type = "System.ConsoleColor"
        self.color = kwargs.get('color')


class RunspacePoolState(object):
    BEFORE_OPEN = 0
    OPENING = 1
    OPENED = 2
    CLOSED = 3
    CLOSING = 4
    BROKEN = 5
    NEGOTIATION_SENT = 6
    NEGOTIATION_SUCCEEDED = 7
    CONNECTING = 8
    DISCONNECTED = 9

    def __init__(self, state):
        """
        [MS-PSRP] 2.2.3.4 RunspacePoolState
        https://msdn.microsoft.com/en-us/library/dd341723.aspx

        Represents the state of the RunspacePool.

        :param state: The state int value
        """
        self.state = state

    def __str__(self):
        return {
            0: "BeforeOpen",
            1: "Opening",
            2: "Opened",
            3: "Closed",
            4: "Closing",
            5: "Broken",
            6: "NegotiationSent",
            7: "NegotiationSucceeded",
            8: "Connecting",
            9: "Disconnected"
        }[self.state]


class PSInvocationState(object):
    NOT_STARTED = 0
    RUNNING = 1
    STOPPING = 2
    STOPPED = 3
    COMPLETED = 4
    FAILED = 5
    DISCONNECTED = 6

    def __init__(self, state):
        """
        [MS-PSRP] 2.2.3.5 PSInvocationState
        https://msdn.microsoft.com/en-us/library/dd341651.aspx

        Represents the state of a pipeline invocation.

        :param state: The state int value
        """
        self.state = state

    def __str__(self):
        return {
            0: "NotStarted",
            1: "Running",
            2: "Stopping",
            3: "Stopped",
            4: "Completed",
            5: "Failed",
            6: "Disconnected"
        }[self.state]


class PSThreadOptions(Enum):
    DEFAULT = 0
    USE_NEW_THREAD = 1
    REUSE_THREAD = 2
    USE_CURRENT_THREAD = 3

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.6 PSThreadOptions
        https://msdn.microsoft.com/en-us/library/dd305678.aspx

        :param value: The enum value for PS Thread Options
        """
        string_map = {
            0: "Default",
            1: "UseNewThread",
            2: "ReuseThread",
            3: "UseCurrentThread"
        }
        super(PSThreadOptions, self).__init__(
            "System.Management.Automation.Runspaces.PSThreadOptions",
            string_map, **kwargs
        )


class ApartmentState(Enum):
    STA = 0
    MTA = 1
    UNKNOWN = 2

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.7 ApartmentState
        https://msdn.microsoft.com/en-us/library/dd304257.aspx

        :param value: The enum value for Apartment State
        """
        string_map = {
            0: 'STA',
            1: 'MTA',
            2: 'UNKNOWN'
        }
        super(ApartmentState, self).__init__(
            "System.Management.Automation.Runspaces.ApartmentState",
            string_map, **kwargs
        )


class RemoteStreamOptions(Enum):
    ADD_INVOCATION_INFO_TO_ERROR_RECORD = 1
    ADD_INVOCATION_INFO_TO_WARNING_RECORD = 2
    ADD_INVOCATION_INFO_TO_DEBUG_RECORD = 4
    ADD_INVOCATION_INFO_TO_VERBOSE_RECORD = 8
    ADD_INVOCATION_INFO = 15

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.8 RemoteStreamOptions
        https://msdn.microsoft.com/en-us/library/dd303829.aspx

        :param value: The initial RemoteStreamOption to set
        """
        super(RemoteStreamOptions, self).__init__(
            "System.Management.Automation.Runspaces.RemoteStreamOptions",
            {}, **kwargs
        )

    @property
    def _to_string(self):
        if self.value == 15:
            return "AddInvocationInfo"

        string_map = (
            ("AddInvocationInfoToErrorRecord", 1),
            ("AddInvocationInfoToWarningRecord", 2),
            ("AddInvocationInfoToDebugRecord", 4),
            ("AddInvocationInfoToVerboseRecord", 8),
        )
        values = []
        for name, flag in string_map:
            if self.value & flag == flag:
                values.append(name)
        return ", ".join(values)

    @_to_string.setter
    def _to_string(self, value):
        pass


class Pipeline(ComplexObject):

    class _ExtraCmds(ComplexObject):
        def __init__(self, **kwargs):
            # Used to encapsulate ExtraCmds in the structure required
            super(Pipeline._ExtraCmds, self).__init__()
            self._extended_properties = (
                ('cmds', ListMeta(
                    name="Cmds",
                    list_value_meta=ObjectMeta("Obj", object=Command),
                    list_types=[
                        "System.Collections.Generic.List`1[["
                        "System.Management.Automation.PSObject, "
                        "System.Management.Automation, Version=1.0.0.0, "
                        "Culture=neutral, PublicKeyToken=31bf3856ad364e35]]",
                        "System.Object",
                    ]
                )),
            )
            self.cmds = kwargs.get('cmds')

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.11 Pipeline
        https://msdn.microsoft.com/en-us/library/dd358182.aspx

        :param is_nested:
        :param commands:
        :param history:
        :param redirect_err_to_out:
        """
        super(Pipeline, self).__init__()
        cmd_types = [
            "System.Collections.Generic.List`1[["
            "System.Management.Automation.PSObject, "
            "System.Management.Automation, "
            "Version=1.0.0.0, Culture=neutral, "
            "PublicKeyToken=31bf3856ad364e35]]",
            "System.Object",
        ]

        self._extended_properties = (
            ('is_nested', ObjectMeta("B", name="IsNested")),
            # ExtraCmds isn't in spec but is value and used to send multiple
            # statements
            ('_extra_cmds', ListMeta(
                name="ExtraCmds",
                list_value_meta=ObjectMeta("Obj", object=self._ExtraCmds),
                list_types=cmd_types
            )),
            ('_cmds', ListMeta(
                name="Cmds", list_value_meta=ObjectMeta("Obj", object=Command),
                list_types=cmd_types
            )),
            ('history', ObjectMeta("S", name="History")),
            ('redirect_err_to_out',
             ObjectMeta("B", name="RedirectShellErrorOutputPipe")),
        )
        self.is_nested = kwargs.get('is_nested')
        self.commands = kwargs.get('cmds')
        self.history = kwargs.get('history')
        self.redirect_err_to_out = kwargs.get('redirect_err_to_out')

    @property
    def _cmds(self):
        # Cmds is always the first statement
        return self._get_statements()[0]

    @_cmds.setter
    def _cmds(self, value):
        # if commands is already set then that means ExtraCmds was present and
        # has already been set
        if self.commands and len(self.commands) > 0:
            return

        # ExtraCmds wasn't present so we need to unpack it
        self.commands = value

    @property
    def _extra_cmds(self):
        statements = self._get_statements()

        # ExtraCmds is only set if we have more than 1 statement, not present
        # if only 1
        if len(statements) < 2:
            return None
        else:
            extra = [self._ExtraCmds(cmds=c) for c in statements]
            return extra

    @_extra_cmds.setter
    def _extra_cmds(self, value):
        # check if extra_cmds was actually set and return if it wasn't
        if value is None:
            return

        commands = []
        for statement in value:
            for command in statement.cmds:
                commands.append(command)
            commands[-1].end_of_statement = True
        self.commands = commands

    def _get_statements(self):
        statements = []
        current_statement = []

        # set the last command to be the end of the statement
        self.commands[-1].end_of_statement = True
        for command in self.commands:
            # need to use deepcopy as the values can be appended to multiple
            # parents and in lxml that removes it from the original parent,
            # whereas this will create a copy of the statement for each parent
            current_statement.append(deepcopy(command))
            if command.end_of_statement:
                statements.append(current_statement)
                current_statement = []

        return statements


class Command(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.12 Command
        https://msdn.microsoft.com/en-us/library/dd339976.aspx

        :param cmd: The cmdlet or script to run
        :param is_script: Whether cmd is a script or not
        :param use_local_scope: Use local or global scope to invoke commands
        :param merge_my_results: Error and Output streams are to be merged on
            pipeline invocation
        :param merge_previous_results: Error and Ouput streams of previous
            commands
        :param merge_error: Merge Error streams with the Output streams
        :param merge_warning: Merge Warning streams with the Output streams
        :param merge_verbose: Merge Verbose streams with the Output streams
        :param merge_debug: Merge Debug streams with the Output streams
        :param args: List of CommandParameters for the cmdlet being invoked
        :param end_of_statement: Whether this command is the last in the
            current statement
        """
        super(Command, self).__init__()
        arg_types = [
            "System.Collections.Generic.List`1[["
            "System.Management.Automation.PSObject, "
            "System.Management.Automation, "
            "Version=1.0.0.0, Culture=neutral, "
            "PublicKeyToken=31bf3856ad364e35]]",
            "System.Object",
        ]
        self._extended_properties = (
            ('cmd', ObjectMeta("S", name="Cmd")),
            ('is_script', ObjectMeta("B", name="IsScript")),
            ('use_local_scope', ObjectMeta("B", name="UseLocalScope")),
            ('merge_my_results', ObjectMeta("Obj", name="MergeMyResult",
                                            object=PipelineResultTypes)),
            # MergeToResults should have the same value as MergeMyResults
            ('merge_my_results', ObjectMeta("Obj", name="MergeToResult",
                                            object=PipelineResultTypes)),
            ('merge_previous_results', ObjectMeta("Obj",
                                                  name="MergePreviousResults",
                                                  object=PipelineResultTypes)),
            ('merge_error', ObjectMeta("Obj", name="MergeError",
                                       object=PipelineResultTypes)),
            ('merge_warning', ObjectMeta("Obj", name="MergeWarning",
                                         object=PipelineResultTypes)),
            ('merge_verbose', ObjectMeta("Obj", name="MergeVerbose",
                                         object=PipelineResultTypes)),
            ('merge_debug', ObjectMeta("Obj", name="MergeDebug",
                                       object=PipelineResultTypes)),
            ('args', ListMeta(
                name="Args",
                list_value_meta=ObjectMeta(object=CommandParameter),
                list_types=arg_types)
             ),
        )
        self.cmd = kwargs.get("cmd")
        self.is_script = kwargs.get("is_script")
        self.use_local_scope = kwargs.get("use_local_scope")

        none_merge = PipelineResultTypes(value=PipelineResultTypes.NONE)
        self.merge_my_results = kwargs.get("merge_my_results", none_merge)
        self.merge_previous_results = kwargs.get("merge_previous_results",
                                                 none_merge)
        self.merge_error = kwargs.get("merge_error", none_merge)
        self.merge_warning = kwargs.get("merge_warning", none_merge)
        self.merge_verbose = kwargs.get("merge_verbose", none_merge)
        self.merge_debug = kwargs.get("merge_debug", none_merge)
        self.args = kwargs.get("args", [])

        # not used in the serialized message but controls how Pipeline is
        # packed (Cmds/ExtraCmds)
        self.end_of_statement = kwargs.get("end_of_statement", False)


class CommandParameter(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.13 Command Parameter
        https://msdn.microsoft.com/en-us/library/dd359709.aspx

        :param name: The name of the parameter, otherwise None
        :param value: The value of the parameter, can be any primitive type
            or Complex Object, Null for no value
        """
        super(CommandParameter, self).__init__()
        self._extended_properties = (
            ('name', ObjectMeta("S", name="N")),
            ('value', ObjectMeta(name="V")),
        )
        self.name = kwargs.get('name')
        self.value = kwargs.get('value')


class _HostDefaultData(ComplexObject):
    class _DictValue(ComplexObject):

        def __init__(self, **kwargs):
            super(_HostDefaultData._DictValue, self).__init__()
            self._extended_properties = (
                ('value_type', ObjectMeta("S", name="T")),
                ('value', ObjectMeta(name="V")),
            )
            self.value_type = kwargs.get('value_type')
            self.value = kwargs.get('value')

    def __init__(self, **kwargs):
        # Used by HostInfo to encapsulate the host info values inside a
        # special object required by PSRP
        super(_HostDefaultData, self).__init__()
        key_meta = ObjectMeta("I32", name="Key")
        self._extended_properties = (
            ('_host_dict', DictionaryMeta(name="data",
                                          dict_key_meta=key_meta)),
        )
        self.host_info = kwargs.get('host_info')

    @property
    def _host_dict(self):
        int_type = "System.Int32"
        str_type = "System.String"

        foreground_color = self.host_info.foreground_color
        background_color = self.host_info.background_color
        cursor_position = self.host_info.cursor_position
        window_position = self.host_info.window_position
        cursor_size = self._DictValue(value_type=int_type,
                                      value=self.host_info.cursor_size)
        buffer_size = self.host_info.buffer_size
        window_size = self.host_info.window_size
        max_window_size = self.host_info.max_window_size
        max_physical_window_size = self.host_info.max_physical_window_size
        window_title = self._DictValue(value_type=str_type,
                                       value=self.host_info.window_title)

        host_dict = (
            (0, foreground_color),
            (1, background_color),
            (2, cursor_position),
            (3, window_position),
            (4, cursor_size),
            (5, buffer_size),
            (6, window_size),
            (7, max_window_size),
            (8, max_physical_window_size),
            (9, window_title),
        )

        return host_dict

    @_host_dict.setter
    def _host_dict(self, value):
        self.host_info = HostInfo()
        self.host_info.foreground_color = value.get(0)
        self.host_info.background_color = value.get(1)
        self.host_info.cursor_position = value.get(2)
        self.host_info.window_position = value.get(3)
        self.host_info.cursor_size = value.get(4)
        self.host_info.buffer_size = value.get(5)
        self.host_info.window_size = value.get(6)
        self.host_info.max_window_size = value.get(7)
        self.host_info.max_physical_window_size = value.get(8)
        self.host_info.window_title = value.get(9)


class HostInfo(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.14 HostInfo
        https://msdn.microsoft.com/en-us/library/dd340936.aspx

        :param foreground_color: Color used to render characters on the screen
            buffer
        :param background_color: Color used to render the background behind
            characters on the screen buffer
        :param cursor_position: Coordinates of the cursor in the screen buffer
        :param window_position: Coordinates of the view window relative to the
            screen buffer. (0, 0) is the upper left of the screen buffer
        :param cursor_size: Cursor size as a percentage
        :param buffer_size: Size of the screen buffer, measured in character
            cells
        :param window_size: Size of the window, measured in character cells
        :param max_window_size: Size of the largest possible window for the
            current buffer
        :param max_physical_window_size: Size of the largest possible window
            ignoring the current buffer dimensions
        :param window_title: String of the title bar text of the current view
            window
        """
        super(HostInfo, self).__init__()
        self._extended_properties = (
            ('_host_data', ObjectMeta("Obj", name="_hostDefaultData",
                                      optional=True, object=_HostDefaultData)),
            ('_is_host_null', ObjectMeta("B", name="_isHostNull")),
            ('_is_host_null', ObjectMeta("B", name="_isHostUINull")),
            ('_is_host_null', ObjectMeta("B", name="_isHostRawUINull")),
            ('_is_host_null', ObjectMeta("B", name="_useRunspaceHost")),
        )
        self.foreground_color = kwargs.get('foreground_color')
        self.background_color = kwargs.get('background_color')
        self.cursor_position = kwargs.get('cursor_position')
        self.window_position = kwargs.get('window_position')
        self.cursor_size = kwargs.get('cursor_size')
        self.buffer_size = kwargs.get('buffer_size')
        self.window_size = kwargs.get('window_size')
        self.max_window_size = kwargs.get('max_window_size')
        self.max_physical_window_size = kwargs.get('max_physical_window_size')
        self.window_title = kwargs.get('window_title')

    @property
    def _is_host_null(self):
        host_null = False
        attributes = ["foreground_color", "background_color",
                      "cursor_position", "window_position", "cursor_size",
                      "buffer_size", "window_size", "max_window_size",
                      "max_physical_window_size", "window_title"]
        for attr in attributes:
            if getattr(self, attr, None) is None:
                host_null = True
                break

        return host_null

    @_is_host_null.setter
    def _is_host_null(self, value):
        pass

    @property
    def _host_data(self):
        if self._is_host_null:
            return None
        else:
            host_data = _HostDefaultData(host_info=self)
            return host_data

    @_host_data.setter
    def _host_data(self, value):
        # need to get the host_info values from the temp _HostDefaultData
        self.foreground_color = value.host_info.foreground_color
        self.background_color = value.host_info.background_color
        self.cursor_position = value.host_info.cursor_position
        self.window_position = value.host_info.window_position
        self.cursor_size = value.host_info.cursor_size
        self.buffer_size = value.host_info.buffer_size
        self.window_size = value.host_info.window_size
        self.max_window_size = value.host_info.max_window_size
        self.max_physical_window_size = \
            value.host_info.max_physical_window_size
        self.window_title = value.host_info.window_title


class ErrorRecord(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.15 ErrorRecord
        https://msdn.microsoft.com/en-us/library/dd340106.aspx
        """
        super(ErrorRecord, self).__init__()
        self._types = [
            "System.Management.Automation.ErrorRecord",
            "System.Object"
        ]
        self._extended_properties = (
            ('exception', ObjectMeta(name="Exception", optional=True)),
            ('target_object', ObjectMeta(name="TargetObject", optional=True)),
            ('invocation', ObjectMeta("B", name="SerializeExtendedInfo")),
            ('invocation_info', ObjectMeta("ObjDynamic", name="InvocationInfo",
                                           object=GenericComplexObject,
                                           optional=True)),
            ('fq_error', ObjectMeta("S", name="FullyQualifiedErrorId")),
            ('category', ObjectMeta("I32", name="ErrorCategory_Category")),
            ('activity', ObjectMeta("S", name="ErrorCategory_Activity",
                                    optional=True)),
            ('reason', ObjectMeta("S", name="ErrorCategory_Reason",
                                  optional=True)),
            ('target_name', ObjectMeta("S", name="ErrorCategory_TargetName",
                                       optional=True)),
            ('target_type', ObjectMeta("S", name="ErrorCategory_TargetType",
                                       optional=True)),
            ('message', ObjectMeta("S", name="ErrorCategory_Message",
                                   optional=True)),
            ('details_message', ObjectMeta("S", name="ErrorDetails_Message",
                                           optional=True)),
            ('action', ObjectMeta("S", name="ErrorDetails_RecommendedAction",
                                  optional=True)),
            ('script_stacktrace', ObjectMeta(
                "S",
                name="ErrorDetails_ScriptStackTrace",
                optional=True
            )),
            ('extended_info_present', ObjectMeta(
                "B", name="SerializeExtendedInfo"
            )),
            ('invocation_name', ObjectMeta(
                "S",
                optional=True,
                name="InvocationInfo_InvocationName"
            )),
            ('invocation_bound_parameters', DictionaryMeta(
                name="InvocationInfo_BoundParameters",
                optional=True,
                dict_key_meta=ObjectMeta("S"),
                dict_types=[
                    "System.Management.Automation.PSBoundParametersDictionary",
                    "System.Collections.Generic.Dictionary`2[[System.String, "
                    "mscorlib, Version=4.0.0.0, Culture=neutral, "
                    "PublicKeyToken=b77a5c561934e089],"
                    "[System.Object, mscorlib, Version=4.0.0.0, "
                    "Culture=neutral, PublicKeyToken=b77a5c561934e089]]",
                    "System.Object"
                ]
            )),
            ('invocation_unbound_arguments', ListMeta(
                name="InvocationInfo_UnboundArguments",
                optional=True,
                list_types=[
                    "System.Collections.Generic.List`1[["
                    "System.Object, mscorlib, Version=4.0.0.0, "
                    "Culture=neutral, PublicKeyToken=b77a5c561934e089]]",
                    "System.Object"
                ]
            )),
            ('invocation_command_origin', ObjectMeta(
                "Obj",
                name="InvocationInfo_CommandOrigin",
                optional=True,
                object=CommandOrigin
            )),
            ('invocation_expecting_input', ObjectMeta(
                "B",
                name="InvocationInfo_ExpectingInput",
                optional=True
            )),
            ('invocation_line', ObjectMeta(
                "S",
                name="InvocationInfo_Line",
                optional=True
            )),
            ('invocation_offset_in_line', ObjectMeta(
                "I32",
                name="InvocationInfo_OffsetInLine",
                optional=True
            )),
            ('invocation_position_message', ObjectMeta(
                "S",
                name="InvocationInfo_PositionMessage",
                optional=True
            )),
            ('invocation_script_name', ObjectMeta(
                "S",
                name="InvocationInfo_ScriptName",
                optional=True
            )),
            ('invocation_script_line_number', ObjectMeta(
                "I32",
                name="InvocationInfo_ScriptLineNumber",
                optional=True
            )),
            ('invocation_history_id', ObjectMeta(
                "I64",
                name="InvocationInfo_HistoryId",
                optional=True
            )),
            ('invocation_pipeline_length', ObjectMeta(
                "I32",
                name="InvocationInfo_PipelineLength",
                optional=True
            )),
            ('invocation_pipeline_position', ObjectMeta(
                "I32",
                name="InvocationInfo_PipelinePosition",
                optional=True
            )),
            ('invocation_pipeline_iteration_info', ListMeta(
                name="InvocationInfo_PipelineIterationInfo",
                optional=True,
                list_value_meta=ObjectMeta("I32"),
                list_types=["System.In32[]", "System.Array", "System.Object"]
            )),
            ('command_type', ObjectMeta(
                "Obj",
                name="CommandInfo_CommandType",
                object=CommandType,
                optional=True,
            )),
            ('command_definition', ObjectMeta(
                "S",
                name="CommandInfo_Definition",
                optional=True,
            )),
            ('command_name', ObjectMeta(
                "S",
                name="CommandInfo_Name",
                optional=True
            )),
            ('command_visibility', ObjectMeta(
                "Obj",
                name="CommandInfo_Visibility",
                object=SessionStateEntryVisibility,
                optional=True
            )),
            ('pipeline_iteration_info', ListMeta(
                name="PipelineIterationInfo", optional=True,
                list_value_meta=ObjectMeta("I32"),
                list_types=[
                    "System.Collections.ObjectModel.ReadOnlyCollection`1[["
                    "System.Int32, mscorlib, Version=4.0.0.0, "
                    "Culture=neutral, PublicKeyToken=b77a5c561934e089]]",
                    "System.Object"
                ]
            )),
        )
        self.exception = kwargs.get('exception')
        self.target_info = kwargs.get('target_info')
        self.invocation = kwargs.get('invocation')
        self.fq_error = kwargs.get('fq_error')
        self.category = kwargs.get('category')
        self.activity = kwargs.get('activity')
        self.reason = kwargs.get('reason')
        self.target_name = kwargs.get('target_name')
        self.target_type = kwargs.get('target_type')
        self.message = kwargs.get('message')
        self.details_message = kwargs.get('details_message')
        self.action = kwargs.get('action')
        self.pipeline_iteration_info = kwargs.get('pipeline_iteration_info')
        self.invocation_name = kwargs.get('invocation_name')
        self.invocation_bound_parameters = \
            kwargs.get('invocation_bound_parameters')
        self.invocation_unbound_arguments = \
            kwargs.get('invocation_unbound_arguments')
        self.invocation_command_origin = \
            kwargs.get('invocation_command_origin')
        self.invocation_expecting_input = \
            kwargs.get('invocation_expecting_input')
        self.invocation_line = kwargs.get('invocation_line')
        self.invocation_offset_in_line = \
            kwargs.get('invocation_offset_in_line')
        self.invocation_position_message = \
            kwargs.get('invocation_position_message')
        self.invocation_script_name = kwargs.get('invocation_script_name')
        self.invocation_script_line_number = \
            kwargs.get('invocation_script_line_number')
        self.invocation_history_id = kwargs.get('invocation_history_id')
        self.invocation_pipeline_length = \
            kwargs.get('invocation_pipeline_length')
        self.invocation_pipeline_position = \
            kwargs.get('invocation_pipeline_position')
        self.invocation_pipeline_iteration_info = \
            kwargs.get('invocation_pipeline_iteration_info')
        self.command_type = kwargs.get('command_type')
        self.command_definition = kwargs.get('command_definition')
        self.command_name = kwargs.get('command_name')
        self.command_visibility = kwargs.get('command_visibility')
        self.extended_info_present = self.invocation is not None


class InformationalRecord(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.16 InformationalRecord (Debug/Warning/Verbose)
        https://msdn.microsoft.com/en-us/library/dd305072.aspx
        """
        super(InformationalRecord, self).__init__()
        self._types = [
            "System.Management.Automation.InformationRecord",
            "System.Object"
        ]
        self._extended_properties = (
            ('message', ObjectMeta("S", name="InformationalRecord_Message")),
            ('invocation', ObjectMeta(
                "B", name="InformationalRecord_SerializeInvocationInfo"
            )),
            ('invocation_name', ObjectMeta(
                "S",
                optional=True,
                name="InvocationInfo_InvocationName"
            )),
            ('invocation_bound_parameters', DictionaryMeta(
                name="InvocationInfo_BoundParameters",
                optional=True,
                dict_key_meta=ObjectMeta("S"),
                dict_types=[
                    "System.Management.Automation.PSBoundParametersDictionary",
                    "System.Collections.Generic.Dictionary`2[[System.String, "
                    "mscorlib, Version=4.0.0.0, Culture=neutral, "
                    "PublicKeyToken=b77a5c561934e089],"
                    "[System.Object, mscorlib, Version=4.0.0.0, "
                    "Culture=neutral, PublicKeyToken=b77a5c561934e089]]",
                    "System.Object"
                ]
            )),
            ('invocation_unbound_arguments', ListMeta(
                name="InvocationInfo_UnboundArguments",
                optional=True,
                list_types=[
                    "System.Collections.Generic.List`1[["
                    "System.Object, mscorlib, Version=4.0.0.0, "
                    "Culture=neutral, PublicKeyToken=b77a5c561934e089]]",
                    "System.Object"
                ]
            )),
            ('invocation_command_origin', ObjectMeta(
                "Obj",
                name="InvocationInfo_CommandOrigin",
                optional=True,
                object=CommandOrigin
            )),
            ('invocation_expecting_input', ObjectMeta(
                "B",
                name="InvocationInfo_ExpectingInput",
                optional=True
            )),
            ('invocation_line', ObjectMeta(
                "S",
                name="InvocationInfo_Line",
                optional=True
            )),
            ('invocation_offset_in_line', ObjectMeta(
                "I32",
                name="InvocationInfo_OffsetInLine",
                optional=True
            )),
            ('invocation_position_message', ObjectMeta(
                "S",
                name="InvocationInfo_PositionMessage",
                optional=True
            )),
            ('invocation_script_name', ObjectMeta(
                "S",
                name="InvocationInfo_ScriptName",
                optional=True
            )),
            ('invocation_script_line_number', ObjectMeta(
                "I32",
                name="InvocationInfo_ScriptLineNumber",
                optional=True
            )),
            ('invocation_history_id', ObjectMeta(
                "I64",
                name="InvocationInfo_HistoryId",
                optional=True
            )),
            ('invocation_pipeline_length', ObjectMeta(
                "I32",
                name="InvocationInfo_PipelineLength",
                optional=True
            )),
            ('invocation_pipeline_position', ObjectMeta(
                "I32",
                name="InvocationInfo_PipelinePosition",
                optional=True
            )),
            ('invocation_pipeline_iteration_info', ListMeta(
                name="InvocationInfo_PipelineIterationInfo",
                optional=True,
                list_value_meta=ObjectMeta("I32"),
                list_types=["System.In32[]", "System.Array", "System.Object"]
            )),
            ('command_type', ObjectMeta(
                "Obj",
                name="CommandInfo_CommandType",
                object=CommandType,
                optional=True,
            )),
            ('command_definition', ObjectMeta(
                "S",
                name="CommandInfo_Definition",
                optional=True,
            )),
            ('command_name', ObjectMeta(
                "S",
                name="CommandInfo_Name",
                optional=True
            )),
            ('command_visibility', ObjectMeta(
                "Obj",
                name="CommandInfo_Visibility",
                object=SessionStateEntryVisibility,
                optional=True
            )),
            ('pipeline_iteration_info', ListMeta(
                name="InformationalRecord_PipelineIterationInfo",
                optional=True,
                list_value_meta=ObjectMeta("I32"),
                list_types=[
                    "System.Collections.ObjectModel.ReadOnlyCollection`1[["
                    "System.Int32, mscorlib, Version=4.0.0.0, "
                    "Culture=neutral, PublicKeyToken=b77a5c561934e089]]",
                    "System.Object"
                ]
            ))
        )
        self.message = kwargs.get('message')
        self.pipeline_iteration_info = kwargs.get('pipeline_iteration_info')
        self.invocation_name = kwargs.get('invocation_name')
        self.invocation_bound_parameters = \
            kwargs.get('invocation_bound_parameters')
        self.invocation_unbound_arguments = \
            kwargs.get('invocation_unbound_arguments')
        self.invocation_command_origin = \
            kwargs.get('invocation_command_origin')
        self.invocation_expecting_input = \
            kwargs.get('invocation_expecting_input')
        self.invocation_line = kwargs.get('invocation_line')
        self.invocation_offset_in_line = \
            kwargs.get('invocation_offset_in_line')
        self.invocation_position_message = \
            kwargs.get('invocation_position_message')
        self.invocation_script_name = kwargs.get('invocation_script_name')
        self.invocation_script_line_number = \
            kwargs.get('invocation_script_line_number')
        self.invocation_history_id = kwargs.get('invocation_history_id')
        self.invocation_pipeline_length = \
            kwargs.get('invocation_pipeline_length')
        self.invocation_pipeline_position = \
            kwargs.get('invocation_pipeline_position')
        self.invocation_pipeline_iteration_info = \
            kwargs.get('invocation_pipeline_iteration_info')
        self.command_type = kwargs.get('command_type')
        self.command_definition = kwargs.get('command_definition')
        self.command_name = kwargs.get('command_name')
        self.command_visibility = kwargs.get('command_visibility')
        self.invocation = False


class HostMethodIdentifier(Enum):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.17 Host Method Identifier
        https://msdn.microsoft.com/en-us/library/dd306624.aspx

        Represents methods to be executed on a host.

        :param value: The method identifier to execute
        """
        string_map = {
            1: "GetName",
            2: "GetVersion",
            3: "GetInstanceId",
            4: "GetCurrentCulture",
            5: "GetCurrentUICulture",
            6: "SetShouldExit",
            7: "EnterNestedPrompt",
            8: "ExitNestedPrompt",
            9: "NotifyBeginApplication",
            10: "NotifyEndApplication",
            11: "ReadLine",
            12: "ReadLineAsSecureString",
            13: "Write1",
            14: "Write2",
            15: "WriteLine1",
            16: "WriteLine2",
            17: "WriteLine3",
            18: "WriteErrorLine",
            19: "WriteDebugLine",
            20: "WriteProgress",
            21: "WriteVerboseLine",
            22: "WriteWarningLine",
            23: "Prompt",
            24: "PromptForCredential1",
            25: "PromptForCredential2",
            26: "PromptForChoice",
            27: "GetForegroundColor",
            28: "SetForegroundColor",
            29: "GetBackgroundColor",
            30: "SetBackgroundColor",
            31: "GetCursorPosition",
            32: "SetCursorPosition",
            33: "GetWindowPosition",
            34: "SetWindowPosition",
            35: "GetCursorSize",
            36: "SetCursorSize",
            37: "GetBufferSize",
            38: "SetBufferSize",
            39: "GetWindowSize",
            40: "SetWindowSize",
            41: "GetWindowTitle",
            42: "SetWindowTitle",
            43: "GetMaxWindowSize",
            44: "GetMaxPhysicalWindowSize",
            45: "GetKeyAvailable",
            46: "ReadKey",
            47: "FlushInputBuffer",
            48: "SetBufferContents1",
            49: "SetBufferContents2",
            50: "GetBufferContents",
            51: "ScrollBufferContents",
            52: "PushRunspace",
            53: "PopRunspace",
            54: "GetIsRunspacePushed",
            55: "GetRunspce",
            56: "PromptForChoiceMultipleSelection"
        }
        super(HostMethodIdentifier, self).__init__(
            "System.Management.Automation.Remoting.RemoteHostMethodId",
            string_map, **kwargs
        )


class CommandType(Enum):
    ALIAS = 0x0001
    FUNCTION = 0x0002
    FILTER = 0x0004
    CMDLET = 0x0008
    EXTERNAL_SCRIPT = 0x0010
    APPLICATION = 0x0020
    SCRIPT = 0x0040
    WORKFLOW = 0x0080
    CONFIGURATION = 0x0100
    ALL = 0x01FF

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.19 CommandType
        https://msdn.microsoft.com/en-us/library/ee175965.aspx

        :param value: The initial flag value for CommandType
        """
        super(CommandType, self).__init__(
            "System.Management.Automation.CommandTypes", {}, **kwargs
        )

    @property
    def _to_string(self):
        if self.value == 0x01FF:
            return "All"

        string_map = (
            ("Alias", 0x0001),
            ("Function", 0x0002),
            ("Filter", 0x0004),
            ("Cmdlet", 0x0008),
            ("ExternalScript", 0x0010),
            ("Application", 0x0020),
            ("Script", 0x0040),
            ("Workflow", 0x0080),
            ("Configuration", 0x0100),
        )
        values = []
        for name, flag in string_map:
            if self.value & flag == flag:
                values.append(name)
        return ", ".join(values)

    @_to_string.setter
    def _to_string(self, value):
        pass


class CommandMetadataCount(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.21 CommandMetadataCount
        https://msdn.microsoft.com/en-us/library/ee175881.aspx

        :param count: The number of CommandMetadata messages in the pipeline
            output
        """
        super(CommandMetadataCount, self).__init__()
        self.types = [
            "Selected.Microsoft.PowerShell.Commands.GenericMeasureInfo",
            "System.Management.Automation.PSCustomObject",
            "System.Object"
        ]
        self._extended_properties = (
            ('count', ObjectMeta("I32", name="Count")),
        )
        self.count = kwargs.get('count')


class CommandMetadata(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.22 CommandMetadata
        https://msdn.microsoft.com/en-us/library/ee175993.aspx

        :param name: The name of a command
        :param namespace: The namespace of the command
        :param help_uri: The URI to the documentation of the command
        :param command_type: The CommandType of the command
        :param output_type: The types of objects that a command can send as
            output
        :param parameters: Metadata of parameters that the command can accept
            as Command Parameters
        """
        super(CommandMetadata, self).__init__()
        self.types = [
            "System.Management.Automation.PSCustomObject",
            "System.Object"
        ]
        self._extended_properties = (
            ('name', ObjectMeta("S", name="Name")),
            ('namespace', ObjectMeta("S", name="Namespace")),
            ('help_uri', ObjectMeta("S", name="HelpUri")),
            ('command_type', ObjectMeta("Obj", name="CommandType",
                                        object=CommandType)),
            ('output_type', ListMeta(
                name="OutputType",
                list_value_meta=ObjectMeta("S"),
                list_types=[
                    "System.Collections.ObjectModel.ReadOnlyCollection`1[["
                    "System.Management.Automation.PSTypeName, "
                    "System.Management.Automation, Version=3.0.0.0, "
                    "Culture=neutral, PublicKeyToken=31bf3856ad364e35]]",
                ]
            )),
            ('parameters', DictionaryMeta(
                name="Parameters",
                dict_key_meta=ObjectMeta("S"),
                dict_value_meta=ObjectMeta("Obj", object=ParameterMetadata))
             ),
        )
        self.name = kwargs.get('name')
        self.namespace = kwargs.get('namespace')
        self.help_uri = kwargs.get('help_uri')
        self.command_type = kwargs.get('command_type')
        self.output_type = kwargs.get('output_type')
        self.parameters = kwargs.get('parameters')


class ParameterMetadata(ComplexObject):

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.23 ParameterMetadata
        https://msdn.microsoft.com/en-us/library/ee175918.aspx

        :param name: The name of a parameter
        :param parameter_type: The type of the parameter
        :param alises: List of alternative names of the parameter
        :param switch_parameter: True if param is a switch parameter
        :param dynamic: True if param is included as a consequence of the data
            specified in the ArgumentList property
        """
        super(ParameterMetadata, self).__init__()
        self.types = [
            "System.Management.Automation.ParameterMetadata",
            "System.Object"
        ]
        self._adapted_properties = (
            ('name', ObjectMeta("S", name="Name")),
            ('parameter_type', ObjectMeta("S", name="ParameterType")),
            ('aliases', ListMeta(
                name="Aliases",
                list_value_meta=ObjectMeta("S"),
                list_types=[
                    "System.Collections.ObjectModel.Collection`1"
                    "[[System.String, mscorlib, Version=4.0.0.0, "
                    "Culture=neutral, PublicKeyToken=b77a5c561934e089]]",
                    "System.Object"
                ])
             ),
            ('switch_parameter', ObjectMeta("B", name="SwitchParameter")),
            ('dynamic', ObjectMeta("B", name="IsDynamic")),
        )
        self.name = kwargs.get('name')
        self.parameter_type = kwargs.get('parameter_type')
        self.aliases = kwargs.get('aliases')
        self.switch_parameter = kwargs.get('switch_parameter')
        self.dynamic = kwargs.get('dynamic')


class CommandOrigin(Enum):
    RUNSPACE = 0
    INTERNAL = 1

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.2.30 CommandOrigin
        https://msdn.microsoft.com/en-us/library/ee441964.aspx

        :param value: The command origin flag to set
        """
        string_map = {
            0: 'Runspace',
            1: 'Internal',
        }
        super(CommandOrigin, self).__init__(
            "System.Management.Automation.CommandOrigin",
            string_map, **kwargs
        )


class PipelineResultTypes(Enum):
    NONE = 0x00
    OUTPUT = 0x01
    ERROR = 0x02
    WARNING = 0x04
    VERBOSE = 0x08
    DEBUG = 0x10
    ALL = 0x20
    NULL = 0x40

    def __init__(self, **kwargs):
        """
        [MS-PSRP] 2.2.3.31 PipelineResultTypes
        https://msdn.microsoft.com/en-us/library/ee938207.aspx

        :param value: The initial PipelineResultType flag to set
        """
        super(PipelineResultTypes, self).__init__(
            "System.Management.Automation.Runspaces.PipelineResultTypes",
            {}, **kwargs
        )

    @property
    def _to_string(self):
        if self.value == 0:
            return "None"
        elif self.value == 0x20:
            return "All"
        elif self.value == 0x40:
            return "Null"

        string_map = (
            ("Output", 0x01),
            ("Error", 0x02),
            ("Warning", 0x04),
            ("Verbose", 0x08),
            ("Debug", 0x10),
        )
        values = []
        for name, flag in string_map:
            if self.value & flag == flag:
                values.append(name)
        return ", ".join(values)

    @_to_string.setter
    def _to_string(self, value):
        pass


class ProgressRecordType(Enum):
    PROCESSING = 0
    COMPLETED = 1

    def __init__(self, **kwargs):
        """
        System.Management.Automation.ProgressRecordType Enum
        This isn't in MS-PSRP but is used in the InformationRecord message and
        so we need to define it here.

        :param value: The initial ProgressRecordType value to set
        """
        string_map = {
            0: 'Processing',
            1: 'Completed',
        }
        super(ProgressRecordType, self).__init__(
            "System.Management.Automation.ProgressRecordType",
            string_map, **kwargs
        )


class SessionStateEntryVisibility(Enum):
    PUBLIC = 0
    PRIVATE = 1

    def __init__(self, **kwargs):
        """
        System.Management.Automation.SessionStateEntryVisibility Enum
        This isn't in MS-PSRP but is used in the InformationalRecord object so
        we need to define it here

        :param value: The initial SessionStateEntryVisibility value to set
        """
        string_map = {
            0: 'Public',
            1: 'Private'
        }
        super(SessionStateEntryVisibility, self).__init__(
            "System.Management.Automation.SessionStateEntryVisibility",
            string_map, **kwargs
        )
