package edu.columbia.cs.ae.feature;

import org.apache.commons.lang3.StringUtils;
import org.w3c.dom.Node;
import org.w3c.dom.NamedNodeMap;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;

public class TextPath {

	/* List of TextNodes that share THIS path */
    private TextNodeList nodeList;
	/* GrandParent Nodes */
    public HashSet<Node> grandparents = new HashSet<Node>();
    /* Aggregate Features */
	private int[] features;

	public TextPath (TextNode n) {
        this.nodeList = new TextNodeList();
        this.features = new int[50];
        add(n);
	}

	public void add (TextNode n) {
        nodeList.add(n);
        grandparents.add(n.grandparent());
		aggregate(n.charFeatures());
	}

	public void aggregate(int[] features) {
		for (int i=0; i<features.length; i++) {
			this.features[i] += features[i];
		}
	}

    public String summary () { return nodeList.summary(); }

    public String toString () { return toString(false); }

	public String toString (boolean printNodeList) {
		String output = "Path: "+path()+" :: "+pid()+"\n";
		output += "Range: "+beginOffset()+"-"+endOffset()+" ("+length()+")\n";
		output += "Aggregate: "+Arrays.toString(this.features)+"\n";
        if (printNodeList) { output += nodeList.toString(); }
		return output;
	}

    public TextNodeList textNodeList () { return nodeList; }
    public HashSet<Node> grandparents () { return grandparents; }
    public int[] features () { return features; }

    public String path () { return nodeList.path(); }
    public String pid () { return nodeList.pid(); }
    public int length () { return nodeList.length(); }
    public int beginOffset () { return nodeList.beginOffset(); }
    public int endOffset () { return nodeList.endOffset(); }
    public int range () { return nodeList.range(); }
}