"""Showcase BeautiPy configuration options for different formatting styles."""

from beautipy import beautify


def main() -> None:
    """Render the same snippet using several configurations."""

    data = "items:[1,2,{kind:complex,value:{raw:'1,2,3'}},[]],meta:{version:1.2,status:ok}"

    print("--- Default ---\n")
    print(beautify(data))
    # output:
    # items: 
    # [
    #     1,
    #     2,
    #     {
    #         kind: complex,
    #         value: 
    #         {
    #             raw: '1,2,3'
    #         }
    #     },
    #     []
    # ],
    # meta: 
    # {
    #     version: 1.2,
    #     status: ok
    # }

    print("\n--- Opener on Same Line ---\n")
    print(beautify(data, opener_same_line=True))
    # output:
    # items: [
    #     1,
    #     2,
    #     {
    #         kind: complex,
    #         value: {
    #             raw: '1,2,3'
    #         }
    #     },
    #     []
    # ],
    # meta: {
    #     version: 1.2,
    #     status: ok
    # }

    print("\n--- Custom Indent ('|   ') ---\n")
    print(beautify(data, indent='|   '))
    # output:
    # items: 
    # [
    # |   1,
    # |   2,
    # |   {
    # |   |   kind: complex,
    # |   |   value: 
    # |   |   {
    # |   |   |   raw: '1,2,3'
    # |   |   }
    # |   },
    # |   []
    # ],
    # meta: 
    # {
    # |   version: 1.2,
    # |   status: ok
    # }

    print("\n--- Blank Lines (depth 1) ---\n")
    # Adds blank lines for top-level items
    print(beautify(data, blank_line_depth=1))
    # output:
    # items: 
    # [
    #     1,
    #     2,
    #     {
    #         kind: complex,
    #         value: 
    #         {
    #             raw: '1,2,3'
    #         }
    #     },
    #     []
    # ],
    #
    # meta: 
    # {
    #     version: 1.2,
    #     status: ok
    # }

    print("\n--- Expanded Empty Structures ---\n")
    print(beautify(data, expand_empty=True))
    # output:
    # items: 
    # [
    #     1,
    #     2,
    #     {
    #         kind: complex,
    #         value: 
    #         {
    #             raw: '1,2,3'
    #         }
    #     },
    #     [
    #     ]
    # ],
    # meta: 
    # {
    #     version: 1.2,
    #     status: ok
    # }


if __name__ == "__main__":
    main()
