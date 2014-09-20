package edu.columbia.cs.ae.feature;

import org.apache.commons.lang3.StringUtils;
import org.w3c.dom.Node;
import org.w3c.dom.NamedNodeMap;
import java.util.ArrayList;
import java.util.Arrays;

public class TextNode {

    /* Path: path of Node names taken to get to this text node */
    private ArrayList<String> path;
    /* Path ID: path of children item #'s taken to get to this text node */
    private ArrayList<Integer> pid;
    /* Node: respective Node in the DOM tree */
    private Node node;
    /* Node Attributes: null */
    private ArrayList<String> attributes;
    /* Parent Attributes: */
    private ArrayList<String> pattributes;
    /* Features: class of features of node text */
    private Features features;

	public TextNode (int nid, int tid, int offset, Node n,
					 ArrayList<String> path, ArrayList<Integer> pid) {
		this.path = path;
		this.pid = pid;
        this.node = n;
        this.pattributes = attributize(n.getParentNode());
        this.features = new Features (text(), tid, nid, offset, path.size());
	}

	public void addFeatures (Features f) { this.features = f; }

    public void addAttribute (String attr) {
        if (attributes == null) { attributes = new ArrayList<String>(); }
        this.attributes.add(attr);
    }

	public void addPattribute (String attr) {
        if (pattributes == null) { pattributes = new ArrayList<String>(); }
        this.pattributes.add(attr);
    }

	public ArrayList<String> attributize (Node n) {
		ArrayList<String> attrList;
		if (n.hasAttributes()) {
			attrList = new ArrayList<String>();
			NamedNodeMap map = n.getAttributes();
			for (int i=0; i<map.getLength(); i++) {
				attrList.add(map.item(i).getNodeName()+": "+map.item(i).getNodeValue());
			}
		} else { attrList = null; }
		return attrList;
	}

	public String toString() {
		String output = "Name: "+name()+" ("+tid()+" "+nid()+" "+offset()+")\n";
		output += "Path: "+strpath()+"\nPID: "+strpid()+"\nText: "+text()+"\n";
		output += "Parent: "+pname()+"\n";
		if (pattributes != null) {
			output += "Parent Attributes:\n";
			for (String s : pattributes) { output += " "+s+"\n"; } 
		}
		output += "Character Features: "+features.charToString()+"\n";
		return output;
	}

    /* GETTER METHODS */

    public int tid () { return this.features.docFeatures()[0]; }
    public int nid () { return this.features.docFeatures()[1]; }
    public int offset () { return this.features.docFeatures()[2]; }
    public int depth () { return this.features.docFeatures()[3]; }
    public ArrayList<String> path () { return this.path; }
    public String strpath () { return StringUtils.join(path.toArray(),"/"); }
    public ArrayList<Integer> pid () { return this.pid; }
    public String strpid () { return StringUtils.join(pid.toArray(),"/"); }
    public Node node () { return this.node; }
    public String name () { return this.node.getNodeName(); } /* Node Name: #text */
    public String text () { return this.node.getNodeValue().trim(); } /* Node Text: content of the text node */
    public int length () { return this.node.getNodeValue().length(); } /* Node Text Length */
    public Node parent () { return this.node.getParentNode(); } /* Parent: parent of this text node */
    public String pname () { return this.node.getParentNode().getNodeName(); } /* Parent Name: */
    public String ptext () { return this.node.getParentNode().getNodeValue(); }  /* Parent Text: */
    public ArrayList<String> pattributes () { return this.pattributes; }
    public Node grandparent() { return parent().getParentNode(); }
    public Features features () { return this.features; }
    public int[] charFeatures() { return this.features.charFeatures(); }
    public int[] docFeatures() { return this.features.docFeatures(); }

}