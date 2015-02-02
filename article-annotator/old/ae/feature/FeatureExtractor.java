package edu.columbia.cs.ae.feature;

import org.apache.commons.lang3.StringUtils;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import java.util.Iterator;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


/**
 * Created with IntelliJ IDEA.
 * User: wojo
 * Date: 6/7/13
 * Time: 7:14 PM
 * To change this template use File | Settings | File Templates.
 */

public class FeatureExtractor {

    private boolean printTextNodeOn;

    private int nodeID;
    private int textID;
    private int offset;

    private TextPathMap textPathMap;

    public FeatureExtractor () { textPathMap = new TextPathMap(); }

    public void traverse (Node n) {
        if (n == null) { throw new IllegalArgumentException("Argument 'node' cannot be null."); }
        traverse(n, new ArrayList<String>(), new ArrayList<Integer>());
    }

    private void traverse (Node n, ArrayList<String> path, ArrayList<Integer> pid) {

        nodeID++;

        if (n.getNodeValue() != null) {
            String value = n.getNodeValue();
            int black = value.replaceAll("\\s+", "").length();
            offset += value.length();

            if (black > 0) {
                TextNode candidate = new TextNode (	nodeID, ++textID, offset, n,
                                                    new ArrayList<String>(path),
                                                    new ArrayList<Integer>(pid));
                if (printTextNodeOn) { System.out.println(candidate.toString()); }
                textPathMap.add(candidate);
            }
        }

		/* TRAVERSE CHILDREN */
        if (n.hasChildNodes()) {
            NodeList children = n.getChildNodes();
            for (int i=0; i<children.getLength(); i++) {
                Node child = children.item(i);
                ArrayList<String> childPath = new ArrayList<String>(path); childPath.add(child.getNodeName());
                ArrayList<Integer> childPid = new ArrayList<Integer>(pid); childPid.add(i);
                traverse(child, childPath, childPid);
            }
        }
    }

    public void setPrintTextNodeOn (boolean printTextNodeOn) { this.printTextNodeOn = printTextNodeOn; }

    public TextPathMap textPathMap () { return textPathMap; }
    public int getNodesTraversed () { return this.nodeID; }
    public int getTextNodesTraversed () { return this.textID; }
    public int getFinalOffset() { return this.offset; }

}
