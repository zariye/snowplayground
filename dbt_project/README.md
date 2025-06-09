Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- `dbt run`
- `dbt test`
  - built-in and custom tests in tests/
- `dbt seeds`
  - to load csv files into database tables and
- analyze
  - `dbt compile`
  - `snowsql -q "$(cat target/compiled/dbt_project/analyses/country_distribution.sql)"` or snowsight worksheet
  - to analyze the project and generate documentation


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
