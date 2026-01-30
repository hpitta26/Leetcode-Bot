"""LeetCode scraper using Playwright"""

from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, expect
import re


class LeetCodeScraper:
    """Scrapes LeetCode user profiles and submission data"""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        """Initialize the scraper"""
        self.headless = headless
        self.timeout = timeout
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
    
    async def start(self):
        """Start the browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        self.context.set_default_timeout(self.timeout)
    
    async def close(self):
        """Close the browser"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    def title_to_slug(self, title: str) -> str:
        """Convert problem title to slug format"""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    async def get_user_recently_solved_problems(self, username: str) -> List[str]:
        """Get list of problem slugs that a user has recently solved"""
        page = await self.context.new_page()
        
        try:
            url = f"https://leetcode.com/u/{username}/"
            await page.goto(url, wait_until='domcontentloaded')
            submission_links = page.locator('a[href^="/submissions/detail/"]')
            
            try:
                await expect(submission_links.first).to_be_visible(timeout=10000)
            except Exception:
                return []
            
            count = await submission_links.count()
            solved_problems = []
            
            for i in range(count):
                link = submission_links.nth(i)
                title_elem = link.locator('[data-title]')
                
                if await title_elem.count() > 0:
                    title = await title_elem.get_attribute('data-title')
                    if title:
                        slug = self.title_to_slug(title)
                        if slug not in solved_problems:
                            solved_problems.append(slug)
            
            return solved_problems
            
        except Exception as e:
            raise Exception(f"Error scraping user '{username}': {str(e)}")
        finally:
            await page.close()
    
    async def check_problem_solved(self, username: str, problem_slug: str) -> bool:
        """Check if a specific problem is solved by a user"""
        try:
            recently_solved = await self.get_user_recently_solved_problems(username)
            return problem_slug in recently_solved
        except Exception as e:
            raise Exception(f"Error checking problem '{problem_slug}' for user '{username}': {str(e)}")
    
    async def get_user_submissions(self, username: str, problem_slugs: List[str]) -> Dict[str, Any]:
        """Get user's submission status for specific problems"""
        submissions = {}
        
        try:
            recently_solved = await self.get_user_recently_solved_problems(username)
            for slug in problem_slugs:
                submissions[slug] = {
                    'solved': slug in recently_solved,
                    'problem_slug': slug
                }
                
        except Exception as e:
            for slug in problem_slugs:
                submissions[slug] = {
                    'solved': False,
                    'problem_slug': slug,
                    'error': str(e)
                }
        
        return {
            'username': username,
            'submissions': submissions
        }
    
    async def scrape_all_users(self, usernames: List[str], problem_slugs: List[str]) -> List[Dict[str, Any]]:
        """Scrape submission data for all users"""
        results = []
        
        for username in usernames:
            try:
                user_data = await self.get_user_submissions(username, problem_slugs)
                results.append(user_data)
            except Exception as e:
                results.append({
                    'username': username,
                    'error': str(e),
                    'submissions': {}
                })
        
        return results

