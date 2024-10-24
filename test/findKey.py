    # def find_key_line_number(key, start_line=0):
    #     for i in range(start_line, len(lines)):
    #         if re.search(rf'"{key}"\s*:', lines[i]):
    #             return i + 1  # Line numbers are 1-indexed
    #     return None

    # def _Walk(aData, aKeys):
    #     i = 0
    #     while i < len(aKeys):
    #         if (isinstance(aData, dict)):
    #             xKey = Keys[i]
    #             if (xKey not in aData):
    #                 return
    #             aData = aData[xKey]
    #             i += 1

    #         elif (isinstance(aData, list)):
    #             for xData in aData:
    #                 xKey = Keys[i]
    #                 if (xData[0] != xKey):
    #                     return

    #                 if (xKey == 'as_dict'):
    #                     aData = xData[1]
    #                 i += 1

    # def Walk(aData, aKeys):
    #     if (isinstance(aData, dict)):
    #         xKey = aKeys[0]
    #         if (xKey in aData):
    #             Walk(aData[xKey], aKeys[1:])
    #     elif (isinstance(aData, list)):
    #         for xData in aData:
    #             if (aKeys):
    #                 xKey = aKeys[0]
    #                 aKeys = aKeys[1:]
    #                 if (xData[0] == xKey):
    #                     if (xKey == 'as_dict'):
    #                         Walk(xData[1], aKeys)

