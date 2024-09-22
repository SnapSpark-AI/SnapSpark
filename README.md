# 🔥 SnapSpark
We developed SnapSpark, an AI-powered wildfire prediction platform that relies on crowdsourced data from images. SnapSpark allows users to upload images of their surroundings, receive predictions, and interact with our map visuals. Our machine learning image analysis is combined with geolocation and environmental data, enabling rapid identification and response to emerging fire threats. SnapSpark makes it easy for anyone, anywhere, to be part of the solution, helping to protect people, property, and the environment.

# 🫡 Our Mission
Our team, driven by a deep concern for both the environment and the safety of our homes, is tackling one of the most pressing natural disaster issues of our time: wildfires. Every year, these infernos ravage 4 to 5 million square kilometers of land globally, releasing a staggering 339 million tons of CO₂ into the atmosphere. While climate change is fuelling the threat of wildfires, the impact of wildfires goes far beyond the environment, simultaneously threatening the safety of our homes and communities. To combat this crisis, we're not only working to develop more accurate and reliable wildfire prediction tools, but we're also incentivizing community members to help us prevent and predict wildfires. Together, we can build a network of vigilant community members, empowered to make a difference.

# 🖥️ Software Layout + File Roles and Specifications

## ⬇️ Backend

| Software          | Role/Action                           | Language |
| ----------------- | ------------------------------------- | -------- |
| ⚡FastAPI        | Web Framework                          | 🐍Python |
| 🐬MySQL          | Database                               | 🥪SQL    |
| 🐳Docker         | Containment                            | N/A      |
| 🤖Roboflow       | CV analysis with about 10k images      | N/A      |
| 🧠Cerebras       | GPT bot for website                    | N/A      |
| 🌧️OpenWeatherMap | Temperature, humidity, and wind speed information per location |           |

| File             | Role/Action                             | Language |
| ---------------- | --------------------------------------- | -------- |
| app.py           | Contains main backend code, shot caller | 🐍Python |
| init_db.py       | Database initializer for MySQL          | 🐍Python |
| Dockerfile       | Software containment recipe             | N/A      |
| requirements.txt | Python dependencies list                | N/A      |

## ⬆️ Frontend

| Software          | Role/Action                           | Language |
| ----------------- | ------------------------------------- | -------- |
| 🥾Bootstrap       | Templating and Design Framework       | 🎨 CSS |

| File             | Role/Action                             | Language |
| ---------------- | --------------------------------------- | -------- |
| script.js        | Communicates with the backend, provides UI | ☕ JavaScript|
| server.go        | Simple HTTP server to host Frontend locally | 🦫 Go |
| style.css       | Styling for index page                   | 🎨 CSS |
| index.html      | Index page text and markup               | 📝 HTML  |
