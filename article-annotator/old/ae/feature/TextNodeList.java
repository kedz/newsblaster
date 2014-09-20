package edu.columbia.cs.ae.feature;

import org.apache.commons.lang3.StringUtils;

import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 * User: wojo
 * Date: 6/25/13
 * Time: 3:41 PM
 * To change this template use File | Settings | File Templates.
 */

public class TextNodeList {

    private ArrayList<TextNode> nodes;

    private int beginOffset;
    private int endOffset;

    public TextNodeList () {
        this.nodes = new ArrayList<TextNode>();
    }

    public void add (TextNode n) {
        nodes.add(n);
        if (length() == 0) { this.beginOffset = n.offset(); }
        this.endOffset = n.offset()+n.length();
    }

    public String summary () {
        String output = ""; int i = 0;
        for (TextNode n : nodes) {
            output += (i++)+" "+n.text()+"\n";
        }
        return output;
    }

    public String toString () {
        String output = "";
        for (TextNode n : nodes) {
            output += n.toString();
        }
        return output;
    }

    public ArrayList<TextNode> textNodes () { return nodes; }
    public TextNode get (int i) { return nodes.get(i); }
    public boolean contains (TextNode n) { return nodes.contains(n); }
    public String path () { return nodes.get(0).strpath(); }
    public String pid () { return nodes.get(0).strpid(); }
    public int length () { return nodes.size(); }
    public int range () { return endOffset-beginOffset; }
    public int depth () { return nodes.get(0).depth(); }
    public int beginOffset () { return beginOffset; }
    public int endOffset () { return endOffset; }

    public ArrayList<String>[] pattributes () {
        ArrayList<String>[] attributes = new ArrayList[length()]; int i=0;
        for (TextNode n : nodes) { attributes[i++] = n.pattributes(); }
        return attributes;
    }

    public Features[] features () {
        Features[] features = new Features[length()]; int i=0;
        for (TextNode n: nodes) { features[i++] = n.features(); }
        return features;
    }

    public int[][] charFeatures () {
        int[][] features = new int[length()][50]; int i=0;
        for (TextNode n : nodes) { features[i++] = n.charFeatures(); }
        return features;
    }

    public int[][] docFeatures () {
        int[][] features = new int[length()][4]; int i=0;
        for (TextNode n : nodes) { features[i++] = n.docFeatures(); }
        return features;
    }

}
