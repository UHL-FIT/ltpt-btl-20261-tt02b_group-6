import pandas as pd
import os
import unicodedata

PETS_FILE = 'data/pets.csv'
WEIGHTS_FILE = 'data/weights.csv'


class PetDataManager:

    """Lớp quản lý dữ liệu thú cưng và cân nặng.

    Chịu trách nhiệm tạo file khi cần, đọc/ghi CSV và
    thực hiện các truy vấn tìm kiếm, cập nhật, xoá.
    """

    def __init__(self):

        # Đảm bảo dữ liệu đã sẵn sàng khi khởi tạo đối tượng.
        self.init_files()

    def init_files(self):

        os.makedirs(
            'data',
            exist_ok=True
        )

        if not os.path.exists(PETS_FILE):

            df = pd.DataFrame(
                columns=[
                    'ID',
                    'Name',
                    'Species',
                    'DOB',
                    'Status',
                    'NextVaccinationDate'
                ]
            )

            df.to_csv(
                PETS_FILE,
                index=False
            )

        if not os.path.exists(WEIGHTS_FILE):

            df = pd.DataFrame(
                columns=[
                    'ID',
                    'PetID',
                    'Date',
                    'Weight'
                ]
            )

            df.to_csv(
                WEIGHTS_FILE,
                index=False
            )

    def get_pets(self):

        """Đọc tất cả thú cưng từ file CSV."""
        return pd.read_csv(PETS_FILE)

    def normalize_text(self, text):

        """Chuẩn hoá văn bản để so sánh không dấu và không phân biệt hoa thường."""
        text = str(text)
        normalized = unicodedata.normalize('NFKD', text)
        return ''.join(
            ch for ch in normalized
            if not unicodedata.combining(ch)
        ).lower()

    def search_pets(self, query, species=None):

        """Tìm thú cưng theo tên/loài và lọc thêm theo loài nếu cần."""
        pets_df = self.get_pets()

        if pets_df.empty:
            return pets_df

        mask = pd.Series(True, index=pets_df.index)

        if query:
            query_normalized = self.normalize_text(query)
            name_match = pets_df['Name'].astype(str).apply(self.normalize_text).str.contains(query_normalized)
            species_match = pets_df['Species'].astype(str).apply(self.normalize_text).str.contains(query_normalized)
            mask &= (name_match | species_match)

        if species:
            species_normalized = self.normalize_text(species)
            mask &= pets_df['Species'].astype(str).apply(self.normalize_text).str.contains(species_normalized)

        return pets_df[mask]

    def get_weights(self):

        """Đọc dữ liệu cân nặng từ file CSV."""
        return pd.read_csv(WEIGHTS_FILE)

    def add_pet(
        self,
        name,
        species,
        dob,
        status,
        next_vac
    ):

        df = self.get_pets()

        new_id = 1 if df.empty else df['ID'].max() + 1

        new_pet = pd.DataFrame([{
            'ID': new_id,
            'Name': name,
            'Species': species,
            'DOB': dob,
            'Status': status,
            'NextVaccinationDate': next_vac
        }])

        df = pd.concat(
            [df, new_pet],
            ignore_index=True
        )

        df.to_csv(
            PETS_FILE,
            index=False
        )

        return new_id

    def delete_pet(self, pet_id):

        pets_df = self.get_pets()

        pets_df = pets_df[
            pets_df['ID'] != pet_id
        ]

        pets_df.to_csv(
            PETS_FILE,
            index=False
        )

        weights_df = self.get_weights()

        weights_df = weights_df[
            weights_df['PetID'] != pet_id
        ]

        weights_df.to_csv(
            WEIGHTS_FILE,
            index=False
        )

    def update_pet(
        self,
        pet_id,
        name,
        species,
        dob,
        status,
        next_vac
    ):

        pets_df = self.get_pets()

        pet_id = int(pet_id)

        pets_df.loc[
            pets_df['ID'] == pet_id,
            ['Name', 'Species', 'DOB', 'Status', 'NextVaccinationDate']
        ] = [name, species, dob, status, next_vac]

        pets_df.to_csv(
            PETS_FILE,
            index=False
        )

    def add_weight(
        self,
        pet_id,
        date,
        weight
    ):

        df = self.get_weights()

        new_id = 1 if df.empty else df['ID'].max() + 1

        new_weight = pd.DataFrame([{
            'ID': new_id,
            'PetID': pet_id,
            'Date': date,
            'Weight': weight
        }])

        df = pd.concat(
            [df, new_weight],
            ignore_index=True
        )

        df.to_csv(
            WEIGHTS_FILE,
            index=False
        )

    def get_weight_history(
        self,
        pet_id
    ):

        weights_df = self.get_weights()

        if weights_df.empty:
            return pd.DataFrame()

        weights_df['PetID'] = weights_df[
            'PetID'
        ].astype(int)

        pet_id = int(pet_id)

        history = weights_df[
            weights_df['PetID'] == pet_id
        ].copy()

        if not history.empty:

            history['Date'] = pd.to_datetime(
                history['Date']
            )

            history = history.sort_values(
                by='Date'
            )

        return history

    def get_monthly_weight_trend(
        self,
        pet_id
    ):

        history = self.get_weight_history(pet_id)

        if history.empty:
            return pd.DataFrame()

        history['Month'] = history['Date'].dt.to_period('M').astype(str)

        trend = history.groupby(
            'Month',
            as_index=False
        )['Weight'].mean()

        trend['Weight'] = trend['Weight'].round(2)

        return trend

    def get_latest_weight(
        self,
        pet_id
    ):

        """Lấy cân nặng gần nhất của thú cưng theo ID."""
        history = self.get_weight_history(
            pet_id
        )

        if history.empty:
            return "Chưa có"

        latest = history.iloc[-1]

        return f"{latest['Weight']} kg"

    def get_statistics(self):

        pets_df = self.get_pets()

        if pets_df.empty:

            return {
                "total": 0,
                "avg_age": 0,
                "warnings": []
            }

        today = pd.to_datetime(
            'today'
        )

        pets_df['DOB'] = pd.to_datetime(
            pets_df['DOB'],
            errors='coerce'
        )

        pets_df['AgeYears'] = (
            today - pets_df['DOB']
        ).dt.days / 365.25

        avg_age = pets_df[
            'AgeYears'
        ].mean()

        pets_df[
            'NextVaccinationDate'
        ] = pd.to_datetime(
            pets_df['NextVaccinationDate'],
            errors='coerce'
        )

        warnings = []

        for _, row in pets_df.iterrows():

            if pd.notna(
                row['NextVaccinationDate']
            ):

                days_until = (
                    row['NextVaccinationDate']
                    - today
                ).days

                if 0 <= days_until <= 14:

                    warnings.append(
                        f"{row['Name']} "
                        f"(Còn {days_until} ngày)"
                    )

                elif days_until < 0:

                    warnings.append(
                        f"{row['Name']} "
                        f"(Quá hạn {-days_until} ngày)"
                    )

        return {
            "total": len(pets_df),
            "avg_age": round(avg_age, 2),
            "warnings": warnings
        }
