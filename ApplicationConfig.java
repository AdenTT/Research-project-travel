package com.bistu.wxapp;

import com.wxapi.model.RequestModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class ApplicationConfig {
    @Bean
    public RestTemplate getRest(){
        return new RestTemplate();
    }

    @Bean
    public RequestModel getRequestModel(){
        RequestModel model = new RequestModel();
        model.setGwUrl("https://way.jd.com/he/freeweather");
        model.setAppkey("76b721baeb93560c31d62b398585fd81");
        return model;
    }
}
