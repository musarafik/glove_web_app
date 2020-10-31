import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
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
    void clickLearn()
    {
        links.get(0).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/learn", obj.getCurrentUrl());
    }

    @Test
    void clickTest()
    {
        links.get(1).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/test", obj.getCurrentUrl());
    }

    @Test
    void clickResources()
    {
        links.get(2).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/additionalResources", obj.getCurrentUrl());
    }

    @Test
    void clickReports()
    {
        links.get(3).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/reports", obj.getCurrentUrl());
    }

    @Test
    void clickAbout()
    {
        links.get(4).click();
        Assertions.assertEquals("http://glove-app.s3-website.us-east-2.amazonaws.com/about", obj.getCurrentUrl());
    }

    @Test
    void learn()
    {
        obj.get("http://glove-app.s3-website.us-east-2.amazonaws.com/learn");
        WebElement word = obj.findElement(By.xpath("//html/body/div/div/div[2]/div/div[2]/div/button[1]"));
        JavascriptExecutor executor = (JavascriptExecutor)obj;
        executor.executeScript("arguments[0].click();", word);

        WebElement monday = obj.findElement(By.xpath("//*[@id=\"root\"]/div/div[2]/div/div[2]/div/button[1]"));
        WebElement tuesday = obj.findElement(By.xpath("/html/body/div/div/div[2]/div/div[2]/div/button[2]"));
        WebElement wednesday = obj.findElement(By.xpath("/html/body/div/div/div[2]/div/div[2]/div/button[3]"));
        WebElement thursday = obj.findElement(By.xpath("/html/body/div/div/div[2]/div/div[2]/div/button[4]"));
        WebElement friday = obj.findElement(By.xpath("/html/body/div/div/div[2]/div/div[2]/div/button[5]"));
        WebElement hello = obj.findElement(By.xpath("/html/body/div/div/div[2]/div/div[2]/div/button[8]"));

        Assertions.assertEquals("Monday", monday.getText());
        Assertions.assertEquals("Tuesday", tuesday.getText());
        Assertions.assertEquals("Wednesday", wednesday.getText());
        Assertions.assertEquals("Thursday", thursday.getText());
        Assertions.assertEquals("Friday", friday.getText());
        Assertions.assertEquals("Hello", hello.getText());
    }

    @Test
    void test()
    {
        obj.get("http://glove-app.s3-website.us-east-2.amazonaws.com/test");
        WebElement word = obj.findElement(By.xpath("/html/body/div/div/div[2]/div/div[2]/button"));
        JavascriptExecutor executor = (JavascriptExecutor)obj;
        executor.executeScript("arguments[0].click();", word);
        List<WebElement> feedback = obj.findElements(By.className("feedbackContainer"));
        Assertions.assertEquals("1", String.valueOf(feedback.size()));
    }
}