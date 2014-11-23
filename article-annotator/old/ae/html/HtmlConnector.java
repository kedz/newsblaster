package edu.columbia.cs.ae.html;

import org.w3c.dom.Document;
import java.io.IOException;
import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import org.xml.sax.SAXException;
import java.net.MalformedURLException;
import java.net.SocketTimeoutException;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created with IntelliJ IDEA.
 * User: wojo
 * Date: 6/6/13
 * Time: 4:52 PM
 * To change this template use File | Settings | File Templates.
 */

public class HtmlConnector {

    private boolean printTimesOn;
    private boolean computeStylesOn;

    private byte[] byteContent;
    private HtmlDocument htmlDocument;
    private Document document;
    private String encoding;

    public HtmlConnector () { this("UTF-8"); }

    public HtmlConnector (String encoding) {
        this.encoding = encoding;
    }

    public byte[] connect (URL url) {
        try {
            if (url == null) {
                throw new IllegalArgumentException ("Argument 'url' cannot be null.");
            }

			/* HTTPURLCONNECTION:
			 *
			 * Subclass of the URLConnection class that provides support for
			 * HTTP-specific features.
			 *
			 * setRequestProperty
			 * setReadTimeout
			 *
			 * getInputStream: Returns an input stream that reads from this open connection.
			 * A SocketTimeoutException can be thrown when reading from the returned input
			 * stream if the read timeout expires before data is available for read.
			 */

            if (printTimesOn) { System.out.print("Opening connection... "); }
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestProperty("User-Agent", "Mozilla; zeep/2.0");
            connection.setRequestProperty("From", "blaster@cs.columbia.edu");
            connection.setReadTimeout(10000);
            if (printTimesOn) { System.out.println("Success!"); }

			/*
			 * BufferedInputStream = reading bytes
			 * BufferedReader = reading characters and lines
			 *
			 * InputStream: reads raw octet (8 bit) data
			 * InputStreamReader: transform data from some encoding into UTF-16
			 */

            if (printTimesOn) { System.out.print("Setup stream... "); }
            BufferedInputStream connectionStream = new BufferedInputStream(connection.getInputStream(), 2048);
            if (printTimesOn) { System.out.println("Success!"); }

			/*
			 * BYTEARRAYOUTPUTSTREAM
			 *
			 * implements an output stream in which the data is written into a byte array
			 *
			 * read(): reads bytes from this byte-input stream into the specified byte array,
			 * starting at the given offset.
			 *
			 * toByteArray(): creates a newly allocated byte array. Its size is the current size of
			 * this output stream and the valid contents of the buffer have been copied into it
			 */

            ByteArrayOutputStream byteStream = new ByteArrayOutputStream();
            byte[] byteBuffer = new byte[2048];
            int readChars = 0;

            if (printTimesOn) { System.out.print("Downloading... "); }
            long start = System.currentTimeMillis();
            while((readChars = connectionStream.read(byteBuffer, 0, 2048)) != -1) {
                byteStream.write(byteBuffer, 0, readChars);
            }
            connectionStream.close();
            long end = System.currentTimeMillis();
            if (printTimesOn) { System.out.println("Done! ["+(end-start)+" ms]"); }

            this.byteContent = byteStream.toByteArray();

            return byteContent;

        } catch (SocketTimeoutException e) {
            System.out.println("Fail!");
            System.err.println(e.getMessage());
            e.printStackTrace();

        } catch (MalformedURLException e) {
            System.out.println("Fail!");
            System.err.println(e.getMessage());
            e.printStackTrace();

        } catch (IOException e) {
            System.out.println("Fail!");
            System.err.println(e.getMessage());
            e.printStackTrace();
        }
        return null;
    }

    public Document parse (byte[] byteContent, URL url) {
        try {
            if (byteContent == null) {
                throw new IllegalArgumentException("Argument 'byteContent' cannot be null.");
            } else if (url == null) {
                throw new IllegalArgumentException ("Argument 'url' cannot be null.");
            }

            if (printTimesOn) { System.out.print("Parsing... "); }
            long start = System.currentTimeMillis();
            this.htmlDocument = new HtmlDocument(byteContent, url, encoding);
            long end = System.currentTimeMillis();
            if (printTimesOn) { System.out.println("Done! ["+(end-start)+" ms]"); }

            if (computeStylesOn) {
                if (printTimesOn) { System.out.print("Computing styles... "); }
                start = System.currentTimeMillis();
                htmlDocument.computeStyle();
                end = System.currentTimeMillis();
                if (printTimesOn) { System.out.println("Done! ["+(end-start)+" ms]"); }
            }

            this.document = htmlDocument.getDocument();
            return document;

        } catch (SAXException e) {
            System.err.println(e.getMessage());
            e.printStackTrace();

        } catch (IOException e) {
            System.err.println(e.getMessage());
            e.printStackTrace();
        }
        return null;
    }

    public String toString () {
        try {
            return new String (byteContent, encoding);
        } catch (IOException e) {
            System.err.println(e.getMessage());
            e.printStackTrace();
        }
        return null;
    }

    public void setPrintTimesOn (boolean printTimesOn) { this.printTimesOn = printTimesOn; }
    public void setComputeStylesOn (boolean computeStylesOn) { this.computeStylesOn = computeStylesOn; }

    public byte[] getByteContent () { return byteContent; }
    public HtmlDocument getHtmlDocument () { return htmlDocument; }
    public Document getDocument () {return document; }

    public static int inputStreamTest () {
        try {
            URL url = new URL("http://www.google.com");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            BufferedInputStream connectionStream = new BufferedInputStream(connection.getInputStream(), 2048);
            int numBytes = connectionStream.available();
            connectionStream.close();
            return numBytes;

        } catch (IOException e) {
            System.err.println(e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
        return -1;
    }
}
