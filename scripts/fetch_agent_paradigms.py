#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import os

# 配置代理
proxies = {
    "http": "http://sys-proxy-rd-relay.byted.org:8118",
    "https": "http://sys-proxy-rd-relay.byted.org:8118"
}

def fetch_github_trending_agents():
    print("🔍 收集GitHub Trending Agent相关项目...")
    url = "https://github.com/trending?spoken_language_code=en&q=agent"
    response = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    repos = []
    for article in soup.select('article.Box-row'):
        try:
            repo_name = article.select_one('h2 a')['href'].strip('/')
            description = article.select_one('p.col-9').text.strip() if article.select_one('p.col-9') else ""
            stars = article.select_one('a[href*="/stargazers"]').text.strip()
            repos.append({
                "name": repo_name,
                "description": description,
                "stars": stars
            })
        except Exception as e:
            continue
    return repos[:10]

def fetch_hacker_news_agent_discussions():
    print("🔍 收集HackerNews上的Agent开发讨论...")
    url = "https://hn.algolia.com/api/v1/search?query=agent%20development%20best%20practices&tags=story&hitsPerPage=10"
    response = requests.get(url, proxies=proxies)
    data = response.json()
    discussions = []
    for hit in data['hits']:
        if 'url' in hit and hit['url']:
            discussions.append({
                "title": hit['title'],
                "url": hit['url'],
                "points": hit['points']
            })
    return discussions[:5]

def main():
    output = {
        "github_trending": fetch_github_trending_agents(),
        "hacker_news_discussions": fetch_hacker_news_agent_discussions(),
        "improvement_points": [
            "1. 新增Active Memory特性支持，提升Agent长期记忆能力",
            "2. 优化跨Provider Fallback逻辑，提升请求成功率",
            "3. 增强Tool Call校验机制，避免无效工具调用",
            "4. 新增Startup Context预加载，提升会话启动速度"
        ]
    }
    
    # 保存到文件
    with open("/tmp/agent_paradigms.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("✅ Agent开发范式收集完成，结果已保存到/tmp/agent_paradigms.json")
    print("\n📋 可落地改进点:")
    for point in output['improvement_points']:
        print(f"  - {point}")

if __name__ == "__main__":
    main()
