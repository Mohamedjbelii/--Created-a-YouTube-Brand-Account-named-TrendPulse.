package com.trendplus.trendplus_backend.config.Database;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;

@Component
public class DatabaseConfig {
    private static final Logger logger = LoggerFactory.getLogger(DatabaseConfig.class);
    @Value("${DB_HOST}")
    private String dbHost;

    @Value("${DB_PORT}")
    private String dbPort;

    @Value("${POSTGRES_DB}")
    private String dbName;

    @Value("${POSTGRES_USER}")
    private String dbUser;

    @Value("${POSTGRES_PASSWORD}")
    private String dbPassword;

    public String getJdbcUrl() {
        return String.format("jdbc:postgresql://%s:%s/%s", dbHost, dbPort, dbName);
    }

    public String getDbUser() {
        return dbUser;
    }

    public String getDbPassword() {
        return dbPassword;
    }

    @Bean
    public DataSource dataSource() {
        logger.warn("testing the env variables : {}/{}/{}/{}",getJdbcUrl(),getDbUser(),getDbUser(),getDbPassword());
        return DataSourceBuilder.create()
                .url(getJdbcUrl())
                .username(getDbUser())
                .password(getDbPassword())
                .driverClassName("org.postgresql.Driver")
                .build();
    }
}