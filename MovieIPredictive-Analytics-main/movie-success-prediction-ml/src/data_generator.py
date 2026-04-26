import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ==========================================
# 1. BOLLYWOOD (Hindi Cinema)
# ==========================================
bollywood_movies = [
    {"title": "Dangal", "budget": 10000000, "revenue": 260000000, "popularity": 85.0, "runtime": 161, "vote_average": 8.4, "genres": [{"name": "Action"}, {"name": "Biography"}, {"name": "Drama"}], "director": "Nitesh Tiwari", "lead_actor": "Aamir Khan", "region": "Bollywood"},
    {"title": "Pathaan", "budget": 30000000, "revenue": 130000000, "popularity": 105.0, "runtime": 146, "vote_average": 6.5, "genres": [{"name": "Action"}, {"name": "Thriller"}], "director": "Siddharth Anand", "lead_actor": "Shah Rukh Khan", "region": "Bollywood"},
    {"title": "Jawan", "budget": 36000000, "revenue": 140000000, "popularity": 115.0, "runtime": 169, "vote_average": 7.0, "genres": [{"name": "Action"}, {"name": "Thriller"}], "director": "Atlee", "lead_actor": "Shah Rukh Khan", "region": "Bollywood"},
    {"title": "Secret Superstar", "budget": 2000000, "revenue": 120000000, "popularity": 60.0, "runtime": 150, "vote_average": 7.9, "genres": [{"name": "Drama"}, {"name": "Music"}], "director": "Advait Chandan", "lead_actor": "Zaira Wasim", "region": "Bollywood"},
    {"title": "Bajrangi Bhaijaan", "budget": 12000000, "revenue": 121000000, "popularity": 75.0, "runtime": 159, "vote_average": 8.1, "genres": [{"name": "Action"}, {"name": "Drama"}, {"name": "Comedy"}], "director": "Kabir Khan", "lead_actor": "Salman Khan", "region": "Bollywood"},
    {"title": "PK", "budget": 12000000, "revenue": 105000000, "popularity": 80.0, "runtime": 153, "vote_average": 8.1, "genres": [{"name": "Comedy"}, {"name": "Drama"}], "director": "Rajkumar Hirani", "lead_actor": "Aamir Khan", "region": "Bollywood"},
    {"title": "Sanju", "budget": 12000000, "revenue": 83000000, "popularity": 65.0, "runtime": 161, "vote_average": 7.7, "genres": [{"name": "Biography"}, {"name": "Drama"}], "director": "Rajkumar Hirani", "lead_actor": "Ranbir Kapoor", "region": "Bollywood"},
    {"title": "Sultan", "budget": 13000000, "revenue": 89000000, "popularity": 72.0, "runtime": 170, "vote_average": 7.0, "genres": [{"name": "Action"}, {"name": "Drama"}, {"name": "Sport"}], "director": "Ali Abbas Zafar", "lead_actor": "Salman Khan", "region": "Bollywood"},
    {"title": "Padmaavat", "budget": 30000000, "revenue": 81000000, "popularity": 68.0, "runtime": 164, "vote_average": 7.0, "genres": [{"name": "Drama"}, {"name": "History"}], "director": "Sanjay Leela Bhansali", "lead_actor": "Ranveer Singh", "region": "Bollywood"},
    {"title": "Animal", "budget": 12000000, "revenue": 108000000, "popularity": 130.0, "runtime": 201, "vote_average": 6.8, "genres": [{"name": "Action"}, {"name": "Crime"}, {"name": "Drama"}], "director": "Sandeep Reddy Vanga", "lead_actor": "Ranbir Kapoor", "region": "Bollywood"},
    # Unsuccessful
    {"title": "Thugs of Hindostan", "budget": 45000000, "revenue": 42000000, "popularity": 60.0, "runtime": 164, "vote_average": 4.1, "genres": [{"name": "Action"}, {"name": "Adventure"}], "director": "Vijay Krishna Acharya", "lead_actor": "Aamir Khan", "region": "Bollywood"},
    {"title": "Zero", "budget": 25000000, "revenue": 23000000, "popularity": 55.0, "runtime": 164, "vote_average": 5.4, "genres": [{"name": "Comedy"}, {"name": "Drama"}, {"name": "Romance"}], "director": "Aanand L. Rai", "lead_actor": "Shah Rukh Khan", "region": "Bollywood"},
    {"title": "Bombay Velvet", "budget": 16000000, "revenue": 5000000, "popularity": 40.0, "runtime": 149, "vote_average": 5.5, "genres": [{"name": "Crime"}, {"name": "Drama"}, {"name": "Thriller"}], "director": "Anurag Kashyap", "lead_actor": "Ranbir Kapoor", "region": "Bollywood"},
    {"title": "Kalank", "budget": 20000000, "revenue": 18000000, "popularity": 48.0, "runtime": 166, "vote_average": 3.6, "genres": [{"name": "Drama"}, {"name": "Romance"}], "director": "Abhishek Varman", "lead_actor": "Varun Dhawan", "region": "Bollywood"},
    {"title": "Bade Miyan Chote Miyan", "budget": 45000000, "revenue": 15000000, "popularity": 55.0, "runtime": 164, "vote_average": 4.5, "genres": [{"name": "Action"}, {"name": "Comedy"}], "director": "Ali Abbas Zafar", "lead_actor": "Akshay Kumar", "region": "Bollywood"},
]

# ==========================================
# 2. TOLLYWOOD (Telugu Cinema)
# ==========================================
tollywood_movies = [
    {"title": "Baahubali 2: The Conclusion", "budget": 35000000, "revenue": 250000000, "popularity": 95.5, "runtime": 167, "vote_average": 8.2, "genres": [{"name": "Action"}, {"name": "Drama"}], "director": "S. S. Rajamouli", "lead_actor": "Prabhas", "region": "Tollywood"},
    {"title": "RRR", "budget": 72000000, "revenue": 160000000, "popularity": 120.0, "runtime": 187, "vote_average": 7.8, "genres": [{"name": "Action"}, {"name": "Drama"}], "director": "S. S. Rajamouli", "lead_actor": "N. T. Rama Rao Jr.", "region": "Tollywood"},
    {"title": "Pushpa: The Rise", "budget": 25000000, "revenue": 50000000, "popularity": 92.0, "runtime": 179, "vote_average": 7.6, "genres": [{"name": "Action"}, {"name": "Crime"}], "director": "Sukumar", "lead_actor": "Allu Arjun", "region": "Tollywood"},
    {"title": "Baahubali: The Beginning", "budget": 25000000, "revenue": 85000000, "popularity": 88.0, "runtime": 159, "vote_average": 8.0, "genres": [{"name": "Action"}, {"name": "Drama"}], "director": "S. S. Rajamouli", "lead_actor": "Prabhas", "region": "Tollywood"},
    {"title": "Salaar", "budget": 30000000, "revenue": 85000000, "popularity": 100.0, "runtime": 175, "vote_average": 6.8, "genres": [{"name": "Action"}, {"name": "Crime"}], "director": "Prashanth Neel", "lead_actor": "Prabhas", "region": "Tollywood"},
    {"title": "Ala Vaikunthapurramuloo", "budget": 10000000, "revenue": 35000000, "popularity": 80.0, "runtime": 165, "vote_average": 7.5, "genres": [{"name": "Action"}, {"name": "Drama"}], "director": "Trivikram Srinivas", "lead_actor": "Allu Arjun", "region": "Tollywood"},
    {"title": "Kalki 2898 AD", "budget": 75000000, "revenue": 130000000, "popularity": 125.0, "runtime": 180, "vote_average": 7.5, "genres": [{"name": "Action"}, {"name": "Sci-Fi"}], "director": "Nag Ashwin", "lead_actor": "Prabhas", "region": "Tollywood"},
    # Unsuccessful
    {"title": "Adipurush", "budget": 60000000, "revenue": 45000000, "popularity": 75.0, "runtime": 179, "vote_average": 3.1, "genres": [{"name": "Action"}, {"name": "Adventure"}], "director": "Om Raut", "lead_actor": "Prabhas", "region": "Tollywood"},
    {"title": "Radhe Shyam", "budget": 40000000, "revenue": 20000000, "popularity": 50.0, "runtime": 138, "vote_average": 4.6, "genres": [{"name": "Drama"}, {"name": "Romance"}], "director": "Radha Krishna Kumar", "lead_actor": "Prabhas", "region": "Tollywood"},
    {"title": "Liger", "budget": 15000000, "revenue": 8000000, "popularity": 45.0, "runtime": 140, "vote_average": 2.7, "genres": [{"name": "Action"}, {"name": "Sport"}], "director": "Puri Jagannadh", "lead_actor": "Vijay Deverakonda", "region": "Tollywood"},
    {"title": "Spyder", "budget": 15000000, "revenue": 11000000, "popularity": 55.0, "runtime": 145, "vote_average": 5.8, "genres": [{"name": "Action"}, {"name": "Thriller"}], "director": "AR Murugadoss", "lead_actor": "Mahesh Babu", "region": "Tollywood"},
    {"title": "Acharya", "budget": 18000000, "revenue": 10000000, "popularity": 45.0, "runtime": 152, "vote_average": 4.2, "genres": [{"name": "Action"}, {"name": "Drama"}], "director": "Koratala Siva", "lead_actor": "Chiranjeevi", "region": "Tollywood"},
]

# ==========================================
# 3. KOLLYWOOD (Tamil Cinema)
# ==========================================
kollywood_movies = [
    {"title": "2.0", "budget": 75000000, "revenue": 85000000, "popularity": 70.0, "runtime": 148, "vote_average": 6.1, "genres": [{"name": "Action"}, {"name": "Sci-Fi"}], "director": "S. Shankar", "lead_actor": "Rajinikanth", "region": "Kollywood"},
    {"title": "Vikram", "budget": 15000000, "revenue": 60000000, "popularity": 85.0, "runtime": 175, "vote_average": 8.3, "genres": [{"name": "Action"}, {"name": "Thriller"}], "director": "Lokesh Kanagaraj", "lead_actor": "Kamal Haasan", "region": "Kollywood"},
    {"title": "Jailer", "budget": 25000000, "revenue": 75000000, "popularity": 90.0, "runtime": 168, "vote_average": 7.3, "genres": [{"name": "Action"}, {"name": "Comedy"}], "director": "Nelson Dilipkumar", "lead_actor": "Rajinikanth", "region": "Kollywood"},
    {"title": "Leo", "budget": 30000000, "revenue": 74000000, "popularity": 95.0, "runtime": 164, "vote_average": 7.4, "genres": [{"name": "Action"}, {"name": "Crime"}], "director": "Lokesh Kanagaraj", "lead_actor": "Vijay", "region": "Kollywood"},
    {"title": "Ponniyin Selvan: I", "budget": 25000000, "revenue": 60000000, "popularity": 80.0, "runtime": 167, "vote_average": 7.6, "genres": [{"name": "Action"}, {"name": "Drama"}], "director": "Mani Ratnam", "lead_actor": "Vikram", "region": "Kollywood"},
    {"title": "Master", "budget": 18000000, "revenue": 38000000, "popularity": 78.0, "runtime": 179, "vote_average": 7.1, "genres": [{"name": "Action"}, {"name": "Thriller"}], "director": "Lokesh Kanagaraj", "lead_actor": "Vijay", "region": "Kollywood"},
    # Unsuccessful
    {"title": "Puli", "budget": 15000000, "revenue": 11000000, "popularity": 45.0, "runtime": 154, "vote_average": 4.1, "genres": [{"name": "Action"}, {"name": "Adventure"}], "director": "Chimbudevan", "lead_actor": "Vijay", "region": "Kollywood"},
    {"title": "Kochadaiiyaan", "budget": 18000000, "revenue": 10000000, "popularity": 50.0, "runtime": 118, "vote_average": 5.4, "genres": [{"name": "Action"}, {"name": "Animation"}], "director": "Soundarya Rajinikanth", "lead_actor": "Rajinikanth", "region": "Kollywood"},
    {"title": "Anjaan", "budget": 10000000, "revenue": 7000000, "popularity": 40.0, "runtime": 170, "vote_average": 4.5, "genres": [{"name": "Action"}, {"name": "Crime"}], "director": "N. Lingusamy", "lead_actor": "Suriya", "region": "Kollywood"},
    {"title": "Beast", "budget": 20000000, "revenue": 19000000, "popularity": 60.0, "runtime": 155, "vote_average": 5.0, "genres": [{"name": "Action"}, {"name": "Thriller"}], "director": "Nelson Dilipkumar", "lead_actor": "Vijay", "region": "Kollywood"},
    {"title": "Valimai", "budget": 18000000, "revenue": 15000000, "popularity": 55.0, "runtime": 178, "vote_average": 5.5, "genres": [{"name": "Action"}, {"name": "Thriller"}], "director": "H. Vinoth", "lead_actor": "Ajith Kumar", "region": "Kollywood"}
]

# Helper function to convert genres
def format_genres(movie_list):
    for m in movie_list:
        m['genres'] = json.dumps(m['genres'])
    return movie_list

bollywood_movies = format_genres(bollywood_movies)
tollywood_movies = format_genres(tollywood_movies)
kollywood_movies = format_genres(kollywood_movies)

# Create DataFrames
df_bollywood = pd.DataFrame(bollywood_movies)
df_tollywood = pd.DataFrame(tollywood_movies)
df_kollywood = pd.DataFrame(kollywood_movies)
df_all = pd.concat([df_bollywood, df_tollywood, df_kollywood], ignore_index=True)

# Save to CSV
df_bollywood.to_csv(os.path.join(DATA_DIR, 'bollywood.csv'), index=False)
df_tollywood.to_csv(os.path.join(DATA_DIR, 'tollywood.csv'), index=False)
df_kollywood.to_csv(os.path.join(DATA_DIR, 'dataset_kollywood.csv'), index=False)
df_all.to_csv(os.path.join(DATA_DIR, 'dataset_indian_all.csv'), index=False)

print(f"Generated bollywood.csv with {len(df_bollywood)} movies.")
print(f"Generated tollywood.csv with {len(df_tollywood)} movies.")
print(f"Generated dataset_kollywood.csv with {len(df_kollywood)} movies.")
print(f"Generated dataset_indian_all.csv with {len(df_all)} movies.")
