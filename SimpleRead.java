// 
// Decompiled by Procyon v0.5.36
// 

package code;

import java.io.IOException;
import java.util.Enumeration;
import javax.comm.SerialPort;
import java.io.InputStream;
import javax.comm.CommPortIdentifier;

public class SimpleRead
{
    private static final char[] COMMAND;
    private static final int WIDTH = 320;
    private static final int HEIGHT = 240;
    private static CommPortIdentifier portId;
    InputStream inputStream;
    SerialPort serialPort;
    
    public static void main(final String[] array) {
        final Enumeration portIdentifiers = CommPortIdentifier.getPortIdentifiers();
        while (portIdentifiers.hasMoreElements()) {
            SimpleRead.portId = portIdentifiers.nextElement();
            if (SimpleRead.portId.getPortType() == 1) {
                System.out.println("Port name: " + SimpleRead.portId.getName());
                if (!SimpleRead.portId.getName().equals("COM3")) {
                    continue;
                }
                final SimpleRead simpleRead = new SimpleRead();
            }
        }
    }
    
    public SimpleRead() {
        final int[][] array = new int[240][320];
        final int[][] array2 = new int[320][240];
        try {
            this.serialPort = (SerialPort)SimpleRead.portId.open("SimpleReadApp", 1000);
            this.inputStream = this.serialPort.getInputStream();
            this.serialPort.setSerialPortParams(1000000, 8, 1, 0);
            int n = 0;
            while (true) {
                System.out.println("Looking for image");
                while (!this.isImageStart(this.inputStream, 0)) {}
                System.out.println("Found image: " + n);
                for (int i = 0; i < 240; ++i) {
                    for (int j = 0; j < 320; ++j) {
                        final int read = this.read(this.inputStream);
                        array[i][j] = ((read & 0xFF) << 16 | (read & 0xFF) << 8 | (read & 0xFF));
                    }
                }
                for (int k = 0; k < 240; ++k) {
                    for (int l = 0; l < 320; ++l) {
                        array2[l][k] = array[k][l];
                    }
                }
                new BMP().saveBMP("c:/out/" + n++ + ".bmp", array2);
                System.out.println("Saved image: " + n);
            }
        }
        catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    
    private int read(final InputStream inputStream) throws IOException {
        final char c = (char)inputStream.read();
        if (c == -1) {
            throw new IllegalStateException("Exit");
        }
        return c;
    }
    
    private boolean isImageStart(final InputStream inputStream, int n) throws IOException {
        return n >= SimpleRead.COMMAND.length || (SimpleRead.COMMAND[n] == this.read(inputStream) && this.isImageStart(inputStream, ++n));
    }
    
    static {
        COMMAND = new char[] { '*', 'R', 'D', 'Y', '*' };
    }
}
