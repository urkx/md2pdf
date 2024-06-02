Ref: https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/PDF32000_2008.pdf

---

# Notes

## PDF Syntax

- PDF Components
    - Objects. 
    - File structure.
    - Document structure.
    - Content streams.

- Non-encrypted PDF can be written in ANSI X3.4-1986.

- Special ASCII-encoded tokens
    - Tokens thar delimit objects, reserved words, certain types of arrays.
    - Data values of strings and streams objects (can be entirely binary data too). Data such as images is represented in binary for compactness.

###  Objects

- Boolean, Integer, Real, String, Name(PDF 1.2), Array, Dictionary(<<>>), Stream(unlimited length), null.

- May be labeled (called an indirect object)

- Indirect objects
    - Identification: Object number, generation number, obj ... endobj

    ```
    10 0 obj
        (String)
    endobj
    ```
    - Reference to an object: Object number, generation number, R keyword
    ```
    12 0 R
    ```
    
- Stream filters (no por el momento)

### File structure



