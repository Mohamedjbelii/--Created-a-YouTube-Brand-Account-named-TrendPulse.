package config.Database;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DatabaseConfig {
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
    @Bean
    public String getJdbcUrl() {
        return String.format("jdbc:postgresql://%s:%s/%s", dbHost, dbPort, dbName);
    }
    @Bean
    public String getDbUser() {
        return dbUser;
    }

    @Bean
    public String getDbPassword() {
        return dbPassword;
    }
}
