package edu.columbia.cs.ae.javascript;

import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.File;
import java.awt.Desktop;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 * User: wojo
 * Date: 6/10/13
 * Time: 3:57 PM
 * To change this template use File | Settings | File Templates.
 */

public class JavaScriptGenerator {

    private final String headerScript = "<script src=\"http://code.jquery.com/jquery.js\"></script>\n";
    private String highlightScript;
    private String documentHtml;

    private Element prime;
    private String selector;
    private String attribute;
    private int level;

    private int nodeID = 0;
    private int textID = 0;

    public JavaScriptGenerator () {}

    public void identify (Node n) { identify(n, 0); }

    private void identify (Node n, int level) {
        if (n.hasChildNodes()) {
            Element e = (Element) n;
            if (e.hasAttribute("id")) {
                this.prime = e;
                this.level = level;
                this.selector = "id";
                this.attribute = e.getAttribute("id");
            } else if (e.hasAttribute("class")) {
                this.prime = e;
                this.level = level;
                this.selector = "class";
                this.attribute = e.getAttribute("class");
            } else {
                identify(n.getParentNode(), ++level);
            }
        }
    }

    public void inspect (Node n) {

        nodeID++;
        System.out.print(nodeID+" "+n.getNodeName());

        if (n.getNodeValue() != null) {

            String value = n.getNodeValue();
            int black = value.replaceAll("\\s+", "").length();

            if (black > 0) {
                textID++;
                System.out.println(" "+textID+" "+value.trim());
            } else if (value.equals("\n\n")) {
                System.out.println(" newline X2");
            } else {
                System.out.println();
            }
        } else {
            System.out.println();
        }

        if (n.hasChildNodes()) {
            NodeList children = n.getChildNodes();
            for (int i=0; i<children.getLength(); i++) {
                inspect(children.item(i));
            }
        }
    }

    public String generate (int idx) {
        if (prime == null) {
            System.err.println("Prime node was not identified.");
            System.exit(1);
        }
        this.highlightScript = "\n<script>\n\t$(document).ready(function(){\n\t\t"+build(idx)+"\n\t});\n</script>\n";
        return highlightScript;
    }

    public String build (int idx) {
        if (level == 0) {
            String output;
            if (selector.equals("id")) {
                output = "$("+attribute+").children('p').eq("+idx+")";
            } else {
                attribute = attribute.trim();
                attribute = attribute.replaceAll("\\s+", ".");
                output = "$(\"."+attribute+"\").children('p').eq("+idx+")";
            }
            output += ".css({\"background-color\" : \"green\",\"color\" : \"#fff\"});";
            return output;
        }
        return null;
    }

    public String inject (String raw) {

        StringBuilder builder = new StringBuilder(raw);

        int end, start = builder.indexOf("<script");
        while (start != -1) {
            end = builder.indexOf("</script>", start);
            builder.delete(start, end+9);
            start = builder.indexOf("<script");
        }

        this.documentHtml = builder.toString();
        documentHtml = documentHtml.replaceAll("</head>", "\n"+headerScript+"\n</head>");
        documentHtml = documentHtml.replaceAll("</body>", "");
        documentHtml = documentHtml.replaceAll("</html>", "");
        documentHtml += highlightScript+"\n</body></html>";

        return documentHtml;
    }

    public void browse () {
        try {
            writeToFile(documentHtml, "test.html");

            File file = new File("/Applications/MAMP/htdocs/test.html");
            Desktop desktop = Desktop.getDesktop();

            desktop.open(file);
        } catch (IOException e) {
            //TODO
        }
    }

    public void writeToFile (String output, String file) {
        try {
            PrintWriter out = new PrintWriter("/Applications/MAMP/htdocs/"+file);
            out.println(output);
            out.close();
        } catch (FileNotFoundException e) {

        }
    }

    public String toString () {
        return this.selector+" "+this.attribute+" ("+this.level+")";
    }

    public String getHeaderScript () { return this.headerScript; }
    public String getHighlightScript () { return this.highlightScript; }
    public String getDocumentHtml () { return this.documentHtml; }

}
