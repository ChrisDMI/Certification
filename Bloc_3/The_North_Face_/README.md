## The North Face Recommender System and Topic Extraction

### Company's Description 📇
The North Face is an American outdoor recreation product company, founded in 1968 to supply climbers. The North Face is known for producing high-quality clothing, footwear, and outdoor equipment. Over the years, it has evolved beyond catering solely to outdoor enthusiasts and has become a fashion symbol in the 2000s.

### Project 🚧
The marketing department at The North Face aims to leverage machine learning solutions to enhance online sales on their website, The North Face France. They have identified two key solutions that can significantly impact conversion rates:

* Recommender System: Deploying a recommender system that suggests additional products to users based on their interests and browsing behavior. The recommender system will enable personalized product recommendations, enhancing the user experience and potentially driving more sales. The recommendations can be displayed as a "You Might Also Be Interested In" section on each product page of the website.

* Topic Extraction: Improving the structure of the product catalog by utilizing topic extraction techniques. The goal is to identify new categories or topics within the product descriptions that could enhance website navigation. By automatically assessing the latent topics present in the item descriptions, The North Face aims to optimize the catalog's organization and make it more user-friendly.

### Goals 🎯
The project is divided into three main steps:

* Grouping Similar Products: Identify groups of products with similar descriptions. By clustering products based on their descriptions, you can group together items that share similar characteristics or attributes.

* Building Recommender System: Utilize the groups of similar products to develop a simple recommender system algorithm. The recommender system will leverage the product clusters to suggest related or complementary items to users, enhancing their shopping experience.

* Topic Modeling: Apply topic modeling algorithms to automatically identify and extract latent topics present in the item descriptions. By uncovering hidden themes or topics, The North Face can gain insights into the catalog's structure and potentially discover new categories that align with customer preferences.

### Scope of this project 🖼️
For this project, you will work with a dataset consisting of item descriptions from The North Face's product catalog. The dataset can be find in `src/`folder
You will explore the dataset, perform data preprocessing and clustering techniques to group similar products. Additionally, you will implement a recommender system algorithm and employ topic modeling algorithms to extract meaningful topics from the item descriptions.