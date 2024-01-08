# HealthJournal

HealthJournal is a open-source, easy-to-use, voice-activated journal designed to track and manage your health records. It's easily accessible, portable, and highly customizable.
![](https://github.com/Hlibisev/healthJournal/blob/main/resources/readme.gif)

## Key Features

### Notion as a Frontend
HealthJournal uses Notion for data rendering and editing. This means that HealthJournal can be opened on any device with a browser. It also implements functionality not available through code, such as saving examination document or medical tests.

Here's how the [Notion template](https://phantom-latency-e69.notion.site/Health-Journal-de4c3203cdbb449ea675089c1dfeaa0b) looks.

![](https://github.com/Hlibisev/healthJournal/blob/main/resources/view.png)

### Backable
Ensure the safety of your health data with weekly backups to AWS, stored in an accessible, human-readable format. HealthJournal guarantees that your information remains independent and easily retrievable, safeguarding health history.

Health is a lifelong journey, and managing your health data is crucial. HealthJournal a strong emphasis on the long-term care and preservation of your health records.

### Portable
Effortlessly access and share your health information with medical professionals. HealthJournal not only facilitates quick retrieval but also offers concise summaries of your overall well-being for the past month, enhancing communication with your healthcare providers.

### Customizable
HealthJournal is designed for easy integration of new features, seamlessly blending into your daily activities, including sports and other routines. In feature it migth be also capable of importing data from various applications, enriching your health journal with comprehensive insights.


## Getting Started

### Prerequisites

- A server with a public IP address.
- An OpenAI API key. Register at [OpenAI](https://platform.openai.com/api-keys) to obtain your key.
- A Notion integration with API key. Set this up at [Notion Developers](https://developers.notion.com/docs/create-a-notion-integration).

### Setup

1. **Notion Template**: Begin by copying and familiarizing yourself with the [Notion template](https://phantom-latency-e69.notion.site/Health-Journal-de4c3203cdbb449ea675089c1dfeaa0b).
2. **Siri Shortcut**: Set up a Siri shortcut pointing to `your_ip/process`. Download it [here](https://www.icloud.com/shortcuts/1e7277cb9bc3439da68453858ae476cb). Set endpoint up and rename it to "Добавь запись".
3. **Environment Configuration**: Populate your `.env` file with the obtained API keys.
    - For a Notion page link like `https://www.notion.so/aeff6b4307b6466e97c8ef023ea79b1f?v=908cd591b39f4dc3bf331739a1bd1532`, the key is `aeff6b4307b6466e97c8ef023ea79b1f`.
4. **Docker**: Launch the Docker file to start the application.
    Установите докер, если у вас он не установлен https://docs.docker.com/engine/install/ubuntu/
    - Ensure Docker is installed on your system. If not installed, follow the instructions at [Docker Installation Guide](https://docs.docker.com/engine/install/ubuntu/).
    - Navigate to the directory where your healthJournal is located.
    - Build the Docker image using the following command:
     ```bash
     docker build . -t health_journal
     ```

    - Once the build is complete, run the container with the following command:
    ```bash
    docker run -p 3332:3332 health_journal
    ```

   - This command maps port 3332 of the container to port 3332 on the host machine, allowing you to access the HealthJournal application.

## Adding Functionality

To add new features to HealthJournal, you need to inherit from `health_journal.processors.Processor` and implement the `should_process` and `process` methods. These methods are applied to each request that comes to the `/process` endpoint. Decorate your class with `@register_processor` to make it visible for server.
You can find implementation examples in `health_journal/processors`.

Additionally, for ease of working with Notion, you can use the `NotionTableProcessor` and `NotionPageProcessor` classes. These support many convenient methods out of the box, including backup and adding entries.

## Support

For support, queries, or contributions, feel free to contact [Hlibisev](https://t.me/hlibisev).
