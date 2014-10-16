package edu.columbia.cs.ae.html;

import org.apache.xerces.parsers.DOMParser;
import org.cyberneko.html.HTMLConfiguration;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import java.io.IOException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.io.FileNotFoundException;
import java.io.ByteArrayInputStream;
import java.io.StringReader;
import java.net.URL;

/*
 * CSSBox is an (X)HTML/CSS rendering engine written in pure Java. Its primary purpose 
 * is to provide a complete and further processable information about the rendered page 
 * contents and layout.
 *
 * The input of the rendering engine is a document DOM tree. The engine is able to 
 * automatically load the style sheets referenced in the document and it computes the 
 * efficient style of each element. Afterwards, the document layout is computed.
 *
 * CSSBox generally expects an implementation of the DOM on its input represented by 
 * its root Document node. The way how the DOM is obtained is not important for CSSBox. 
 * However, in most situations, the DOM is obtained by parsing a HTML or XML file. 
 * Therefore, CSSBox provides a framework for binding a parser to the layout engine. 
 * Moreover it contains a default parser implementation that may be simply used or it 
 * can be easily replaced by a custom implementation when required. The default 
 * implementation is based on the NekoHTML parser and Xerces 2. 
 */

import org.fit.cssbox.css.DOMAnalyzer;
import org.fit.cssbox.css.NormalOutput;
import org.fit.cssbox.css.Output;
import org.fit.cssbox.css.CSSNorm;

public class HtmlDocument {

  private Document document;
  private URL source;

  public HtmlDocument(byte[] content, URL url, String encoding) throws SAXException, IOException {

      if (url == null) {
          throw new IllegalArgumentException ("Argument 'url' cannot be null.");
      }

      if (content == null) {
          throw new IllegalArgumentException ("Argument 'content' cannot be null.");
      }

      source = url;

      /* 
       * DOM parser using the NekoHTML parser configuration
       *
       * http://cyberneko.org/html/properties/names/elems 
       * Specifies how the NekoHTML components should modify recognized element names.
       * Names can be converted to upper-case, converted to lower-case, or left as-is.
       * The value of "match" specifies that element names are to be left as-is but the
       * end tag name will be modified to match the start tag name. This is required to
       * ensure that the parser generates a well-formed XML document.
       *
       * http://cyberneko.org/html/properties/default-encoding 
       * Sets the default encoding the NekoHTML scanner should use when parsing documents.
       * In the absence of an http-equiv directive in the source document, this setting is
       * important because the parser does not have any support to auto-detect the encoding.
       */ 

      DOMParser parser = new DOMParser(new HTMLConfiguration());
      parser.setProperty("http://cyberneko.org/html/properties/names/elems", "lower");
      parser.setProperty("http://cyberneko.org/html/properties/default-encoding", encoding);

      /*
       * BYTEARRAYINPUTSTREAM
       * allows a buffer in the memory to be used as an InputStream. The input sources is a
       * byte array. An internal counter keeps track of the next byte to be supplied by the
       * read method.
       *
       * INPUTSOURCE
       * A single input source for an XML entity. This class allows a SAX application to
       * encapsulate information about an input source in a single object, which may include
       * a public identifier, a system identifier, a byte stream (possibly with a specified
       * encoding), and/or a character stream.
       */

      InputSource inputSource = new InputSource(new ByteArrayInputStream(content));
      parser.parse(inputSource);
      
      /*
       * The Document Object Model is a platform and language-neutral interface that will 
       * allow programs and scripts to dynamically access and update the content, structure 
       * and style of documents. The document can be further processed and the results of 
       * that processing can be incorporated back into the presented page
       */

      this.document = parser.getDocument(); // DOM document object
      document.getDocumentElement().normalize();
  }

  /*
   * attributesToStyles(): method converts some HTML presentation attributes to CSS 
   * styles (e.g. the <font> tag attributes, table attributes and some more).
   * 
   * addStyleSheet(): method used to add a style sheet to the document. The style sheet 
   * is passed as a text string containing the CSS code. In our case, we add two built-in 
   * style sheets that represent the standard document style. These style sheets are 
   * imported as the user agent style sheets according to the CSS specification. 
   * 
   * getStyleSheets(): method loads and processes all the internal and external style 
   * sheets referenced from the document including the inline style definitions. In 
   * case of external style sheets, CSSBox tries to obtain the file from the 
   * corresponding URL, if accessible.
   *
   * stylesToDomInherited: method encodes the efficient style of all the elements to 
   * their <code>style</code> attributes while applying the inheritance. This is 
   * currently not necessary for the rendering. It is practical mainly together with
   * the <code>printTagTree</code> method for debugging the resulting style. 
   */

  public void computeStyle() {
    DOMAnalyzer domAnalyzer = new DOMAnalyzer(document, source);
    domAnalyzer.attributesToStyles(); //convert the HTML presentation attributes to inline styles
    domAnalyzer.addStyleSheet(null, CSSNorm.stdStyleSheet(), DOMAnalyzer.Origin.AGENT); // use the standard style sheet
    domAnalyzer.addStyleSheet(null, CSSNorm.userStyleSheet(), DOMAnalyzer.Origin.AGENT); // use the additional style sheet
    domAnalyzer.getStyleSheets(); // load the author style sheets
    domAnalyzer.stylesToDomInherited();

    System.out.println(domAnalyzer.toString());
  }

  public void writeToFile(String filename) throws FileNotFoundException {
      Output out = new NormalOutput(document);
      out.dumpTo(new PrintStream(new FileOutputStream(filename,true)));
  }

  public NodeList getListOfLinks() { return document.getElementsByTagName("a"); }

  public NodeList getListOfParagraphs() { return document.getElementsByTagName("p"); }

  public Document getDocument() { return document; }

}