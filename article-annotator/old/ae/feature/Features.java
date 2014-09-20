package edu.columbia.cs.ae.feature;

import java.util.Arrays;

/**
 * Created with IntelliJ IDEA.
 * User: wojo
 * Date: 6/25/13
 * Time: 12:45 PM
 * To change this template use File | Settings | File Templates.
 */

public class Features {

    /* Character Features: character features of node text */
    private int[] charFeatures;
    /* Document Features: relative document position of node */
    private int[] docFeatures = new int[4];

    public Features (String text, int tid, int nid, int offset, int depth) {
        this.charFeatures = Charmander.computeCharFeatures(text);
        this.docFeatures[0] = tid;  /* Node ID: ith Node traversed in the DOM tree */
        this.docFeatures[1] = tid;  /* TextNode ID: ith TextNode traversed in the DOM tree */
        this.docFeatures[2] = tid;  /* Offset: position relative to document */
        this.docFeatures[3] = tid;  /* Depth: depth of node in the DOM tree */
    }

    public String charToString () { return Arrays.toString(charFeatures); }
    public String docToString () { return Arrays.toString(docFeatures); }

    public int[] charFeatures () { return charFeatures; }
    public int[] docFeatures () { return docFeatures; }
}
