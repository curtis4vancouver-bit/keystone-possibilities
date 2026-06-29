# 📋 Sister Site Setup Blueprint: Google Indexing API for Keystone [[possibilities|Possibilities]]

Use this step-by-step guide tomorrow to set up instant indexing for **keystonepossibilities.ca** in under 10 minutes, bypassing the Google Cloud account sync bug.

---

## 🛠️ Step 1: Add the Service Account as an Owner in GSC

1. Open Google Search Console for `keystonepossibilities.ca`.
2. Go to **Settings** -> **Users and permissions**.
3. Click **ADD USER**.
4. Enter the service account email: 
   `vertex-express@semiotic-ion-458504-e9.iam.gserviceaccount.com`
5. Click the **Permission** dropdown and select **Owner** (do not select *Full* or *Restricted*).
6. Click **ADD**. 
7. *Verify*: Confirm the table displays `vertex-express` as **Owner** in the list.

---

## 🔌 Step 2: Configure WordPress (Keystone Possibilities)

1. Log into your WordPress admin panel for `keystonepossibilities.ca`.
2. Go to **Plugins** -> **Add New**, search for **Instant Indexing for Google** by Rank Math, install and activate it.
3. Navigate to **Rank Math SEO** -> **Instant Indexing** -> **Google API Settings** tab.
4. Copy the entire contents of the service account JSON key file:
   `C:\Users\Curtis\Downloads\semiotic-ion-458504-e9-1771d6c71093.json`
5. Paste the JSON key directly into the **Google JSON Key** textarea.
6. Select checkboxes for **Posts**, **Pages**, and **Media**.
7. Click **Save Changes**.

---

## 🚀 Step 3: Trigger First Indexing & Verify

1. Go to the **Console** tab of the Instant Indexing settings.
2. Fetch the XML sitemap for the new site (e.g., `/sitemap_index.xml` or `/post-sitemap.xml`).
3. Paste the URLs into the text field.
4. Select the **Google: Publish/update URL** radio button.
5. Click **Send to API**.
6. *Verify*: Ensure a green **Success** notice appears and that the Google API remaining quota reduces, proving a successful connection!
