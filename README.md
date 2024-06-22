# Md2Pdf

Export Markdown files to PDF.
Implementing official PDF specification

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

- Stream objects
    - Consist of a dictionary followed by a stream object
    ```
    dictionary
    stream
    ...bytes...
    endstream
    ```
    - All streams shall be indirect objects and the stream dictionary shall be a direct object.
    - Stream dictionary entries:
      
    | Key | Value |
    | ---- | ----- |
    | Length | (Required) Number of bytes of the stream |
    | Filter | (Optional) Name of the filter to apply to stream data |
    | DecodeParams | (Optional) Dictionary or array of dictionaries used by the filter specified in Filter |
    | F | (Optional) File containing the stream data |
    | FFilter | (Optional) Filter to apply to stream data contained in file F |
    | FDecodeParams | (Optional) Params of FFilter |
    | DL | (Optional) Number of bytes in the decoded (defiltered) stream |

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
    10 0 R
    ```
    
- Stream filters (no por el momento)

### File structure

- Header. One line identifying PDF specification of the file.

- Body. Objects of the document.

- Xref table. Info about indirect objects in the file.

- Trailer. Location of the Xref table and of certain special objects within the body.

