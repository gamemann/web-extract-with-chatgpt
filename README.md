A Linux [Python](https://www.python.org/) project that extracts data from a website using [Selenium](https://www.selenium.dev/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), sends the data through [OpenAI](https://openai.com/)'s [ChatGPT](https://openai.com/index/chatgpt/) API, and returns the result.

As of right now, that only websites this project can extract data from are topics from Discourse forums (using the [`discourse_topic`](./src/extract/extractors/discourse_topic.py) extractor) since that's what I used when testing this application. You may create your own extractors as well, please take a look at the source code [here](./src/extract/) for more information.

Before making this project, I created a private project for my modding [community](https://moddingcommunity.com) that utilized the above technologies which inspired me to make this open source project. I'm hoping the code in the repository helps other developers who want to integrate ChatGPT into their projects or wants to see how to parse and extract data from websites.

![Preview](./preview/preview01.gif)

## Requirements
* An OpenAI key which may be retrieved after setting up billing from [here](https://platform.openai.com/signup).
* The URL to a web page that supports extracting data from one of the extractors [here](./src/extract/extractors).

### Firefox Geckodriver
In order for Selenium to operate, you need the Firefox Geckodriver which may be found [here](https://github.com/mozilla/geckodriver/releases) along with the `firefox-esr` package.

```bash
# Download Geckodriver 0.35.0 driver.
wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz

# Extract Geckodriver binary.
tar -xzvf geckodriver-v0.35.0-linux64.tar.gz

# Move binary to /usr/bin.
sudo mv geckodriver /usr/bin

# Install the Firefox ESR package using apt (for Debian/Ubuntu-based systems).
sudo apt install -y firefox-esr
```

### Python
Python (version 3 or higher) is required to run this project. Additionally, the following Python packages are required.

```
selenium==4.27.1
beautifulsoup4==4.12.3
requests==2.32.3
Jinja2==3.1.4
openai==1.57.4
```

You may install these packages using the following command.

```bash
pip3 install -r requirements.txt
```

#### Python Virtual Environment
I recommend running this project within a virtual environment in Python. You can create a virtual environment using the following command assuming you have the required Python packages on your server.

```bash
python3 -m venv venv/
```

You can then activate the virtual environment and install the required packages listed above inside of the environment.

```bash
# Activate virtual environment.
source venv/bin/activate

# Download required packages in new environment.
pip3 install -r requirements.txt
```

## Command Line Usage
The following command line arguments are supported.

| Name | Default | Description |
| ---- | ------- | ----------- |
| -c --cfg | `./conf.json` | Path to config file. |
| -l --list | N/A | Lists contents of the config settings and exits. |
| -h --help | N/A | Prints the help menu and exits. |

<details>
    <summary>Example(s)</summary>

### Load Custom Config
```bash
python3 src/main.py -c /etc/mycustomconf.json
```

### List config settings.
```bash
python3 src/main.py -l
```

### Print help menu.
```bash
python3 src/main.py --help
```
</details>

## Configuration
The default configuration file is located at `./conf.json`, but can be changed with the command line arguments mentioned above. I recommend copying the [`conf.ex.json`](./conf.ex.json) file to `conf.json` for new users.

Here is a list of configuration settings.

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
| save_to_fs | bool | `false` | Saves config to file system after parsing. This is good for automatic formatting and saving all available settings to config file. |
| extract | Extract Object | `{}` | The extract object (read below). |
| chatgpt | ChatGPT Object | `{}` | The ChatGPT object (read below). |
| output | Output Object | `{}` | The output object (read below). |

<details>
    <summary>Example(s)</summary>

### Save To Filesystem
```json
{
    "save_to_fs": true,
    "extract": {},
    "chatgpt": {},
    "output": {}
}
```
</details>

### Extract Object
The extract object contains settings related to extracting the web data.

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
| drv_path | string | `/usr/bin/geckodriver` | The path to the Geckodriver binary file. |
| agents | string array | `[]` | A list of user agents to randomly select from when sending web request. |

<details>
    <summary>Example(s)</summary>

#### Use Custom User Agents
```json
{
    "agents":
    [
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    ]
}
```
</details>

### ChatGPT Object
The ChatGPT object contains settings related to OpenAI and ChatGPT.

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
| key | string | `null` | The OpenAI key (required). |
| model | string | `gpt-3.5-turbo` | The ChatGPT model to use. |
| max_tokens | int | `500` | The maximum tokens to use with the request. |
| temperature | float | `0.7` | The temperature to use with the ChatGPT request. Read more about this [here](https://aimresearch.co/leaders-opinion/leaders-opinion-how-temperature-affects-chatgpt-with-rachael-chudoba). |
| max_input | int | `500` | The maximum characters to send to ChatGPT. |

Here is a list of model code names you can use with the `model` setting.

```
gpt-3.5-turbo
gpt-3.5-turbo-16k
gpt-4
gpt-4-32k
gpt-4o
gpt-4o-mini
o1-mini
o1
o1-pro
```

**NOTE** - There are multiple models you may use including GPT-4o and GPT-4o-mini. However, I've found the newer models are **very** expensive with the API compared to GPT-3. Therefore, I recommend using the GPT-3 model when you can. For a list of models, check [here](https://platform.openai.com/docs/models/gp)! For information on pricing, check [here](https://openai.com/api/pricing/)!

<details>
    <summary>Example(s)</summary>

#### Use GPT-4o (EXPENSIVE!)
```json
{
    "key": "CHANGEME",
    "model": "gpt-4o",
    "max_tokens": 500,
    "temperature": 0.5,
    "max_input": 1000
}
```
</details>

## Output Object
The output object is used for sending the ChatGPT response somewhere.

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
| type | string | `stdout` | The type of output to use (`stdout` or `post` are supported right now). |
| post | Post Object | `{}` | Settings for the POST type. |

When a POST request is sent, the content type is `application/json` and an example of the request body may be found below.

```json
{
    "response": "<ChatGPT Response>"
}
```

### Post Object
The POST object contains settings when using the `post` type to send the ChatGPT response to a web endpoint via a POST request.

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |
| url | string | `http://localhost` | The URL to send the POST request to. |
| headers | Dictionary <string, string> | `{}` | Headers to send with the request. |

<details>
    <summary>Example(s)</summary>

#### Send POST Request With Auth Token
```json
{
    "type": "post",
    "post": {
        "url": "https://api.mydomain.com/web-extract",
        "headers": {
            "Authorization": "Bearer <MY TOKEN>"
        }
    }
}
```
</details>

## Running
You can run this program from the main repository's directory using the following command.

```bash
python3 src/main.py
```

## Notes
### Template System For ChatGPT Role & Prompt
A basic template system is used when formatting what role and prompt to send ChatGPT. Templates may be found in the [`templates/`](./templates/) directory.

The variables `url` and `content` are passed to the templates, so feel free to use them (e.g. `{{ content }}`).

## Credits
* [Christian Deacon](https://github.com/gamemann)