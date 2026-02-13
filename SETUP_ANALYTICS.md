# How to Set Up Google Analytics 4 (GA4)

To track visits on your website (**La French Barcelona**), the standard free tool is **Google Analytics**.

## Step 1: Create a Google Analytics Account
1. Go to [analytics.google.com](https://analytics.google.com/).
2. Click **Start measuring**.
3. **Account Name**: Enter "La French Barcelona".
4. **Property Name**: Enter "La French Website".
5. **Time Zone**: Select "Spain" time.
6. **Currency**: Euro (€).

## Step 2: Get Your Measurement ID
1. During setup, choose platform: **Web**.
2. **Website URL**: Enter `lafrench-barcelona.com` (or your domain).
3. **Stream Name**: "La French Website".
4. Click **Create stream**.
5. You will see a **Measurement ID** starting with `G-XXXXXXXXXX`. **Copy this ID.**

## Step 3: Add Code to Website
I have already prepared the code in your `index.html` file. You just need to paste your ID there.

1. Open `index.html`.
2. Look for the comment `<!-- Google Analytics (GA4) -->` near the top (in the `<head>` section).
3. Replace `G-XXXXXXXXXX` with your actual ID.
4. Uncomment the code block if it is commented out.

## Step 4: Verify
1. Deploy your site.
2. Open your website in a new tab.
3. Go back to Google Analytics -> **Reports** -> **Realtime**.
## Step 5: Recommended Dashboards

Once data starts flowing (approx. 24-48h for full reports), use these views:

### 1. The "Traffic Acquisition" Report (Best for Marketing)
*   **Where**: Reports > Acquisition > Traffic acquisition
*   **What it tells you**: "Where did my users come from?" (Google, Instagram, Direct).
*   **Key Metric**: Look at **Engaged sessions** and **Events per session**.

### 2. The "Realtime" Dashboard (Best for Testing)
*   **Where**: Reports > Realtime
*   **What it tells you**: Who is on the site *right now*. Perfect for testing if your ads are running.

### 3. Looker Studio (For Custom Dashboards)
If GA4 is too complex, you can connect your data to **Google Looker Studio** (free) to create a simple, visual 1-page report.
*   **Template**: Search for "GA4 Standard Report Template" in Looker Studio.
*   **Key Widgets to add**:
    *   Total Users (Scorecard)
    *   Sessions by Source (Pie Chart)
    *   Event Count for "click" (to track WhatsApp clicks)
