package edu.columbia.cs.ae.feature;

/**
 * Created with IntelliJ IDEA.
 * User: wojo
 * Date: 6/25/13
 * Time: 4:42 PM
 * To change this template use File | Settings | File Templates.
 */
public class TextPathTest {


    private static boolean parag;       /* Contains <p> tag in path */
    private static boolean link;        /* Contains <a>, <b>, <i>, <em>, or <strong> tag in path */
    private static boolean corrupt;     /* Contains a corrupt tag in path */

    public static boolean isNoise (TextPath tap) {
        boolean noise = false;              /* Indicates that path is noisey */
        boolean narrow = isNarrow(tap);     /* Range of offset is greater than zero */
        boolean charse = isCharse(tap);     /* Character density is low */
        boolean bad = inspectTags(tap);     /* Indicates bad path */
        if (bad || narrow || charse) {
            noise = true;
        }
        return noise;
    }

    public static boolean isNarrow (TextPath tap) {
        boolean narrow = false;
        if (tap.range() == 0) { narrow = true; }
        return narrow;
    }

    public static boolean isCharse (TextPath tap) {
        boolean charse = false;
        if (tap.features()[0] < 400) { charse = true; }
        return charse;
    }

    public static boolean inspectTags (TextPath tap) {
        corrupt = false; link = false; parag = false;
        String[] tags = tap.path().split("/");
        for (int i=0; i<tags.length; i++) {
            if (tags[i].equals("script") ||
                    tags[i].equals("#comment") ||
                    tags[i].equals("nav") ||
                    tags[i].equals("form") ||
                    tags[i].equals("style") ||
                    tags[i].equals("h1") ||
                    tags[i].equals("h2") ||
                    tags[i].equals("h3") ||
                    tags[i].equals("h4") ||
                    tags[i].equals("h5") ||
                    tags[i].equals("h6")) {		// aside, footer, select, label
                corrupt = true;
                break;
            } else if ( tags[i].equals("a") ||
                    tags[i].equals("b") ||
                    tags[i].equals("i") ||
                    tags[i].equals("em") ||
                    tags[i].equals("strong")) {
                link = true;
            } else if (tags[i].equals("p")) {
                parag = true;
            }
        }
        return !parag || link || corrupt;
    }
}
