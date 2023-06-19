package ut.com.ds.usermanager;

import org.junit.Test;
import com.ds.usermanager.api.MyPluginComponent;
import com.ds.usermanager.impl.MyPluginComponentImpl;

import static org.junit.Assert.assertEquals;

public class MyComponentUnitTest
{
    @Test
    public void testMyName()
    {
        MyPluginComponent component = new MyPluginComponentImpl(null);
        assertEquals("names do not match!", "myComponent",component.getName());
    }
}