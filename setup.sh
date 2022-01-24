mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"chansamuelys@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = 443\n\
" > ~/.streamlit/config.toml