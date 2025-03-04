<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 15: Open Source Endpoints through Hugging Face</h1>

### [Quicklinks](https://github.com/AI-Maker-Space/AIE5/00_AIM_Quicklinks)

| 🤓 Pre-work | 📰 Session Sheet | ⏺️ Recording     | 🖼️ Slides        | 👨‍💻 Repo         | 📝 Homework      | 📁 Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|
| [Session 15: Pre-Work](https://www.notion.so/Session-15-Intro-to-Production-and-Open-Source-Endpoints-189cd547af3d80168768dc2a8e18cfed?pvs=4#189cd547af3d816b8edce736371f4e47)| [Session 15: Intro to Production and Open-Source Endpoints](https://www.notion.so/Session-15-Intro-to-Production-and-Open-Source-Endpoints-189cd547af3d80168768dc2a8e18cfed) | Coming Soon! | Coming Soon! | You Are Here! | Coming Soon! | [AIE5 Feedback 3/4](https://forms.gle/gMZfY2oHmeYMhWmn6) |


In today's assignment, we'll be creating an Open Source LLM-powered LangChain RAG Application in Chainlit.

There are 2 main sections to this assignment:

## Build 🏗️

### Build Task 1: Deploy LLM and Embedding Model to SageMaker Endpoint Through Hugging Face Inference Endpoints

#### LLM Endpoint

Select "Inference Endpoint" from the "Solutions" button in Hugging Face:

![image](https://i.imgur.com/G8yK2OC.png)

Create a "+ New Endpoint" from the Inference Endpoints dashboard.

![image](https://i.imgur.com/Gukctmv.png)

Select the `NousResearch/Meta-Llama-3.1-8B-Instruct` model repository and name your endpoint. Select N. Virginia as your region (`us-east-1`). Give your endpoint an appropriate name. Make sure to select *at least* a L4 GPU. 

![image](https://i.imgur.com/ruF7ssQ.png)

Select the following settings for your `Container Configuration`.

![image](https://i.imgur.com/10deNnA.png)

Create a `Protected` endpoint.

![image](https://i.imgur.com/GUni11E.png)

If you were successful, you should see the following screen:

![image](https://i.imgur.com/sKowQt8.png)

#### Embedding Model Endpoint
We'll be using `Snowflake/snowflake-arctic-embed-m` for our embedding model today.

The process is the same as the LLM - but we'll make a few specific tweaks:

Let's make sure our set-up reflects the following screenshots:

![image](https://i.imgur.com/EFPd6jr.png)

After which, make sure the advanced configuration is set like so:

![image](https://i.imgur.com/v3qkc0H.png)

> #### NOTE: PLEASE SHUTDOWN YOUR INSTANCES WHEN YOU HAVE COMPLETED THE ASSIGNMENT TO PREVENT UNESSECARY CHARGES.

### Build Task 2: Create RAG Pipeline with LangChain

Follow the [notebook](https://colab.research.google.com/drive/1v1FYmvKH4gsqcdZwIT9wvbQe0GUjrc9d?usp=sharing) to create a LangChain pipeline powered by Hugging Face endpoints!

Once you're done - please move on to Build Task 3!

### Build Task 3: Create a Chainlit Application

1. Create a new empty Docker space through Hugging Face - with the following settings:

![image](https://i.imgur.com/0YzyQX7.png)

> NOTE: You may notice the application builds slowly (~15min.) with the default free-tier hardware. The process will be faster using the `CPU upgrade` Space Hardware - though it is not required. 

2. Clone the newly created space into a directory that is *NOT IN YOUR AI MAKERSPACE REPOSITORY* using the SSH option.

> NOTE: You may need to ensure you've added your SSH key to Hugging Face, as well as GitHub. This should already be done.

![image](https://i.imgur.com/5RyBdP5.png)

3. Copy and Paste (`cp ...` or through UI) the contents of `Week 8/Day 2` into the newly cloned repository. 

> NOTE: Please keep the `README.md` that was cloned from your space and delete the class `README.md`.

4. Using the `ls` command or the `tree` command verify that you have copied over: 
 - `app.py`
 - `Dockerfile`
 - `data/paul_graham_essays.txt`
 - `chainlit.md`
 - `.gitignore`
 - `.env.sample`
 - `solution_app.py`
 - `requirements.txt`

 Here is an example as the `ls -al` CLI command: 

 ![image](https://i.imgur.com/vazGYeb.png)

 5. Work through the `app.py` file to migrate your LCEL LangChain RAG Chain from the Notebook to Chainlit!

 6. Be sure to modify your `README.md` and `chainlit.md` as you see fit!

 > NOTE: If you get stuck, there is a working reference version in `solution_app.py`.

 7. When you are done with local testing - push your changes to your space. 

 8. Make sure you add your `HF_LLM_ENDPOINT`, `HF_EMBED_ENDPOINT`, `HF_TOKEN` as "Secrets" in your Hugging Face Space.

### Terminating Your Resources

Please head to the settings of each endpoint and select `Delete Endpoint`. You will need to type the name of the endpoint to delete the resources.

### Deliverables

- Completed Notebook
- Chainlit Application in a Hugging Face Space Powered by Hugging Face Endpoints
- Screenshot of endpoint usage

Example Screen Shot:

![image](https://i.imgur.com/qfbcVpS.png)

## Ship 🚢

Create a Hugging Face Space powered by Hugging Face Endpoints!

### Deliverables

- A short Loom of the space, and a 1min. walkthrough of the application in full

## Share 🚀

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped a open-source LLM-powered Retrieval Augmented Generation Application with LangChain! 🎉🤖

🔍 Three Key Takeaways:
1️⃣ 
2️⃣ 
3️⃣ 

Let's continue pushing the boundaries of what's possible in the world of AI and question-answering. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#LangChain #QuestionAnswering #RetrievalAugmented #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```

> #### NOTE: PLEASE SHUTDOWN YOUR INSTANCES WHEN YOU HAVE COMPLETED THE ASSIGNMENT TO PREVENT UNESSECARY CHARGES.
