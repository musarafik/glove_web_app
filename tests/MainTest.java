import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.safari.SafariDriver;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class MainTest {
    WebDriver obj;
    List<WebElement> links;

    @org.junit.jupiter.api.BeforeEach
    void setUp() {
        obj = new SafariDriver();
        obj.manage().window().maximize();
        obj.get("http://glove-app.s3-website.us-east-2.amazonaws.com/");
        links = obj.findElements(By.className("nav-link"));

    }

    @org.junit.jupiter.api.AfterEach
    void tearDown() {
        obj.quit();
    }

    @Test
    void clickLearn(){
        links.get(0).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/learn", obj.getCurrentUrl());
    }

    @Test
    void clickTest(){
        links.get(1).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/test", obj.getCurrentUrl());
    }

    @Test
    void clickResources(){
        links.get(2).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/additionalResources", obj.getCurrentUrl());
    }

    @Test
    void clickReports(){
        links.get(3).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/reports", obj.getCurrentUrl());
    }

    @Test
    void clickAbout(){
        links.get(4).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/about", obj.getCurrentUrl());
    }

    @Test
    void learn()
    {
        links.get(0).click();
        String winBefore = obj.getWindowHandle();
        for(String handle : obj.getWindowHandles())
        {
            obj.switchTo().window(handle);
        }
        obj.manage().window().maximize();
        List<WebElement> words = obj.findElements(By.className("wordsButton btn btn-secondary"));
        WebElement word = obj.findElement(By.name("Words"));
        words.get(0).click();
        WebElement monday = obj.findElement(By.name("Monday"));
        Assertions.assertEquals("Monday", monday.getText());
    }
}