
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

@st.cache_resource
def load_data():
    df = pd.read_csv("data_beasiswa.csv")
    return df

@st.cache_resource
def train_model(df):
    X = df.drop("Kelayakan_Beasiswa", axis=1)
    y = df["Kelayakan_Beasiswa"]

    categorical_cols = ["Penghasilan_Ortu", "Organisasi", "Prestasi"]
    numeric_cols = ["IPK", "Jumlah_Tanggungan"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", "passthrough", numeric_cols),
        ]
    )

    clf = DecisionTreeClassifier(random_state=42, max_depth=5)
    model = Pipeline(steps=[("preprocessor", preprocessor),
                           ("classifier", clf)])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    return model, accuracy

def main():
    st.title("Sistem Pendukung Keputusan Beasiswa Mahasiswa")
    st.write("Metode: **Klasifikasi (Decision Tree)**")
    st.write(
        "Aplikasi ini membantu menentukan kelayakan calon penerima beasiswa "
        "berdasarkan data akademik dan ekonomi."
    )

    df = load_data()
    model, accuracy = train_model(df)

    menu = st.sidebar.radio(
        "Menu",
        ["Deskripsi Sistem", "Lihat Data", "Prediksi Kelayakan", "Tentang Pembuat"]
    )

    if menu == "Deskripsi Sistem":
        st.subheader("Deskripsi Sistem")
        st.markdown(
            """
            **Tujuan:**  
            Membantu pihak kampus/instansi dalam mengambil keputusan kelayakan penerima beasiswa.

            **Input yang digunakan:**  
            - IPK  
            - Penghasilan Orang Tua  
            - Jumlah Tanggungan  
            - Keaktifan Organisasi  
            - Prestasi Akademik / Non-Akademik  

            **Metode:**  
            - Menggunakan *Decision Tree Classifier* dari scikit-learn  
            - Fitur kategorikal diproses dengan *OneHotEncoder*  
            - Data dibagi menjadi data latih dan data uji (80:20)

            **Performa Model:**  
            - Akurasi pada data uji: **{:.2f}%**
            """.format(accuracy * 100)
        )

    elif menu == "Lihat Data":
        st.subheader("Data Beasiswa")
        st.dataframe(df)
        st.write("Jumlah data:", df.shape[0])
        st.write("Jumlah fitur:", df.shape[1] - 1)

        st.markdown("**Distribusi Kelas Kelayakan:**")
        st.bar_chart(df["Kelayakan_Beasiswa"].value_counts())

    elif menu == "Prediksi Kelayakan":
        st.subheader("Prediksi Kelayakan Beasiswa")

        st.markdown("### Input Data Calon Penerima Beasiswa")

        col1, col2 = st.columns(2)

        with col1:
            ipk = st.slider("IPK", min_value=2.0, max_value=4.0, value=3.25, step=0.01)
            penghasilan = st.selectbox(
                "Penghasilan Orang Tua (per bulan)",
                ["<=2jt", "2-5jt", ">5jt"]
            )
            tanggungan = st.slider("Jumlah Tanggungan Keluarga", 1, 10, 3)

        with col2:
            organisasi = st.selectbox(
                "Keaktifan Organisasi",
                ["Tidak Aktif", "Aktif"]
            )
            prestasi = st.selectbox(
                "Prestasi",
                ["Tidak ada", "Lokal", "Nasional", "Internasional"]
            )

        input_data = pd.DataFrame(
            {
                "IPK": [ipk],
                "Penghasilan_Ortu": [penghasilan],
                "Jumlah_Tanggungan": [tanggungan],
                "Organisasi": [organisasi],
                "Prestasi": [prestasi],
            }
        )

        if st.button("Prediksi Kelayakan"):
            prediction = model.predict(input_data)[0]
            proba = model.predict_proba(input_data)[0]

            st.markdown("### Hasil Prediksi")
            if prediction == "Layak":
                st.success("Calon penerima **LAYAK** mendapatkan beasiswa.")
            else:
                st.error("Calon penerima **TIDAK LAYAK** mendapatkan beasiswa.")

            st.markdown("### Probabilitas Prediksi")
            st.write(
                {
                    model.classes_[0]: f"{proba[0]*100:.2f}%",
                    model.classes_[1]: f"{proba[1]*100:.2f}%",
                }
            )

    elif menu == "Tentang Pembuat":
        st.subheader("Tentang Pembuat")
        st.write("Nama: Isi dengan nama kamu")
        st.write("NIM: Isi dengan NIM kamu")
        st.write("Mata Kuliah: Sistem Pendukung Keputusan")
        st.write("Metode: Klasifikasi - Decision Tree")

        st.markdown(
            "Silakan sesuaikan bagian ini dengan identitasmu sebelum pengumpulan tugas."
        )

if __name__ == "__main__":
    main()
