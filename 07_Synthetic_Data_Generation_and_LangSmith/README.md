
<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

## <h1 align="center" id="heading">Session 7: Synthetic Data Generation and LangSmith</h1>

| 🤓 Pre-work | 📰 Session Sheet | ⏺️ Recording     | 🖼️ Slides        | 👨‍💻 Repo         | 📝 Homework      | 📁 Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|
| [Session 7: Pre-Work](https://www.notion.so/Session-7-Synthetic-Data-Generation-for-Evaluation-189cd547af3d8085ab5dc89d7b5c0879?pvs=4#189cd547af3d8103b7f2c5d9a383686a)| [Session 7: Synthetic Data Generation for Evaluation](https://www.notion.so/Session-7-Synthetic-Data-Generation-for-Evaluation-189cd547af3d8085ab5dc89d7b5c0879) |  [Recording](https://us02web.zoom.us/rec/share/rPTLLyth_oyE_7-aXWJoHnxKsg-UPHDrszdw5ny6ng7-l_DuX3M0W86THS2q2n-w.VL8kpsdpEOibmlg0) (1Q@@y#AD) | [Session 7: Synthetic Data Generation for Evaluation](https://www.canva.com/design/DAGcIQhny7k/unM4iPJ1HN83c18xRnnhBQ/edit?utm_content=DAGcIQhny7k&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) | You Are Here! | [Session 7: Synthetic Data Generation for Evaluation](https://forms.gle/erEBQJ3LoBnjFYFX6) | [AIE5 Feedback 2/4](https://forms.gle/E8iXiLwwpPCd49dx8) |

In today's assignment, we'll be creating Synthetic Data, and using it to benchmark (and improve) a LCEL RAG Chain.

- 🤝 BREAKOUT ROOM #1
  1. Use RAGAS to Generate Synthetic Data

- 🤝 BREAKOUT ROOM #2
  1. Load them into a LangSmith Dataset
  2. Evaluate our RAG chain against the synthetic test data
  3. Make changes to our pipeline
  4. Evaluate the modified pipeline
    
The notebook Colab link is located [here](https://colab.research.google.com/drive/1XgotHE4BHcnhSIkj1-2lLoMGDJZM0pmh?usp=sharing)

## Ship 🚢

The completed notebook!

#### 🏗️ BONUS ACTIVITY (FULL MARKS IF COMPLETED IN LIEU OF ABOVE NOTEBOOK):

Reproduce the RAGAS Synthetic Data Generation Steps - but utilize a LangGraph Agent Graph, instead of the Knowledge Graph approach.

This generation should leverage the [Evol Instruct](https://arxiv.org/pdf/2304.12244) method to generate synthetic data.

Your final state (output) should contain (at least, not limited to):

1. `List(dict)`: Evolved Questions, their IDs, and their Evolution Type.
2. `List(dict)`: Question IDs, and Answer to the referenced Evolved Question.
3. `List(dict)`: Question IDs, and the relevant Context(s) to the Evolved Question.

The Graph should handle:

1. Simple Evolution.
2. Multi-Context Evolution.
3. Reasoning Evolution.

It should take, as input, a list of LangChain Documents.

### Deliverables

- A short Loom of the notebook, and a 1min. walkthrough of the application in full

## Share 🚀

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped Synthetic Data Generation, benchmarking, and iteration with RAGAS & LangChain! 🎉🤖

🔍 Three Key Takeaways:
1️⃣ 
2️⃣ 
3️⃣ 

Let's continue pushing the boundaries of what's possible in the world of AI and question-answering. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#LangChain #QuestionAnswering #RetrievalAugmented #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```
