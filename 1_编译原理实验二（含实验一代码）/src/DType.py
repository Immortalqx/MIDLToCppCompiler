class DType:
    # signed int
    SHORT = "short"
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    LONG = "long"
    LONG_LONG = "long long"
    # unsigned int
    UNSIGNED_SHORT = "unsigned short"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    UINT64 = "uint64"
    UNSIGNED_LONG = "unsigned long"
    UNSIGNED_LONG_LONG = "unsigned long long"
    # float pt
    FLOAT = "float"
    DOUBLE = "double"
    LONG_DOUBLE = "long double"
    # text
    CHAR = "char"
    STRING = "string"
    # boolean
    BOOLEAN = "boolean"

    @staticmethod
    def is_signed_int(str_: str):
        if str_ == DType.SHORT or \
                str_ == DType.INT8 or \
                str_ == DType.INT16 or \
                str_ == DType.INT32 or \
                str_ == DType.INT64 or \
                str_ == DType.LONG or \
                str_ == DType.LONG_LONG:
            return True
        return False

    @staticmethod
    def is_unsigned_int(str_: str):
        if str_ == DType.UNSIGNED_SHORT or \
                str_ == DType.UINT8 or \
                str_ == DType.UINT16 or \
                str_ == DType.UINT32 or \
                str_ == DType.UINT64 or \
                str_ == DType.UNSIGNED_LONG or \
                str_ == DType.UNSIGNED_LONG_LONG:
            return True
        return False

    @staticmethod
    def is_float_pt(str_: str):
        if str_ == DType.FLOAT or \
                str_ == DType.DOUBLE or \
                str_ == DType.LONG_DOUBLE:
            return True
        return False

    @staticmethod
    def is_text(str_: str):
        if str_ == DType.CHAR or str_ == DType.STRING:
            return True
        return False

    # 这个函数可能并没有用！！！
    @staticmethod
    def is_BOOLEAN(str_: str):
        if str_ == DType.BOOLEAN:
            return True
        return False

    @staticmethod
    def to_signed_int(str_: str):
        if str_ == DType.UNSIGNED_SHORT:
            return DType.SHORT
        elif str_ == DType.UINT8:
            return DType.INT8
        elif str_ == DType.UINT16:
            return DType.INT16
        elif str_ == DType.UINT32:
            return DType.INT32
        elif str_ == DType.UINT64:
            return DType.INT64
        elif str_ == DType.UNSIGNED_LONG:
            return DType.LONG
        elif str_ == DType.UNSIGNED_LONG_LONG:
            return DType.LONG_LONG
