package edu.columbia.cs.ae.feature;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

/**
 * Created with IntelliJ IDEA.
 * User: wojo
 * Date: 6/25/13
 * Time: 2:50 PM
 * To change this template use File | Settings | File Templates.
 */

public class TextPathMap {

    private HashMap<String,TextPath> textPathMap;
    private HashMap<String,TextPath> filteredMap;

    public TextPathMap () {
        textPathMap = new HashMap<String, TextPath>();
    }

    public void add (TextNode textNode) {
        String key = textNode.strpath();
        TextPath textPath;
        if (textPathMap.containsKey(key)) {
            textPath = textPathMap.get(key);
            textPath.add(textNode);
        } else { textPath = new TextPath(textNode); }
        textPathMap.put(key, textPath);
    }

    public HashMap filter () {
        filteredMap = (HashMap<String,TextPath>) textPathMap.clone();
        for (Iterator<Map.Entry<String,TextPath>> it = filteredMap.entrySet().iterator(); it.hasNext();) {
            Map.Entry<String,TextPath> entry = it.next();
            //String key = entry.getKey();
            TextPath val = entry.getValue();
            if (TextPathTest.isNoise(val)) {
                it.remove();
            }
        }
        return filteredMap;
    }

    public HashMap<String,TextPath> textPathMap () { return textPathMap; }
    public HashMap<String,TextPath> filteredMap () { return filteredMap; }
}
