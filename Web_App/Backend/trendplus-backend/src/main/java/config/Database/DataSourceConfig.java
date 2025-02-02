package config.Database;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;

@Configuration
@EnableConfigurationProperties(DatabaseConfig.class)
public class DataSourceConfig {
    private final DatabaseConfig databaseConfig;

    public DataSourceConfig(DatabaseConfig databaseConfig) {
        this.databaseConfig = databaseConfig;
    }
    @Bean
    public DataSource dataSource() {
        return DataSourceBuilder.create()
                .url(databaseConfig.getJdbcUrl())
                .username(databaseConfig.getDbUser())
                .password(databaseConfig.getDbPassword())
                .driverClassName("org.postgresql.Driver")
                .build();
    }

}
