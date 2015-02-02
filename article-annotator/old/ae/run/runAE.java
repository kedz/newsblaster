package edu.columbia.cs.ae.run;

import edu.columbia.cs.ae.feature.*;
import edu.columbia.cs.ae.html.*;
import edu.columbia.cs.ae.javascript.*;

/**
 * Created with IntelliJ IDEA.
 * User: wojo
 * Date: 6/7/13
 * Time: 9:43 PM
 * To change this template use File | Settings | File Templates.
 */

import edu.columbia.cs.ae.javascript.JavaScriptGenerator;
import org.w3c.dom.Node;
import org.w3c.dom.Document;
import java.io.IOException;
import java.net.URL;

public class runAE {

    private static boolean printTimesOn = false;
    private static boolean computeFeaturesOn = true;

    public static void main(String[] args) {

        String link;
        if (args.length > 0) { link = args[0]; }
        else { link = "http://www.wired.com/opinion/2013/06/why-i-have-nothing-to-hide-is-the-wrong-way-to-think-about-surveillance/"; }

        try {
            URL url = new URL(link);

            HtmlConnector zeep = new HtmlConnector();
            zeep.setPrintTimesOn(printTimesOn);

            byte[] byteContent = zeep.connect(url);
            Document doc = zeep.parse(byteContent, url);

            if (doc == null) {
                System.err.println("Variable 'document' cannot be null.");
                System.exit(1);
            }

            Node root = doc.getDocumentElement(); 	// HTML NODE
            Node body = root.getLastChild(); 		// BODY NODE

            FeatureExtractor droid = new FeatureExtractor();
            droid.traverse(body);

            if (computeFeaturesOn) {

                TextPath best = (TextPath) droid.textPathMap().filter().values().iterator().next();

                //TextPath best = droid.filter();
                System.out.println("Best: "+best.path());
                System.out.println("Best #nodes: "+best.length());
                System.out.println("Parents: "+best.grandparents().size());

                JavaScriptGenerator gen = new JavaScriptGenerator();

                System.out.println(best.summary());


                for (Node n : best.grandparents) {
                    System.out.println("*****");
                    gen.inspect(n);
                }

                //gen.identify(best.parent);
                //gen.inspect(best.parent);
                //gen.generate(1);

                //System.out.println("Attribute: "+gen.toString());
                //System.out.println("Javascript:\n"+gen.getHighlightScript());

                //String output = zeep.toString();
                //gen.inject(output);
                //gen.browse();
            }

        } catch (IOException e) {
            System.err.println(e.getMessage());
            e.printStackTrace();
        }
    }
}
