from app.database.mysql import get_mysql_connection


def create_document(document_id: str,filename: str,file_path: str,status: str,):
    connection = get_mysql_connection()

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO documents (
                document_id,
                filename,
                file_path,
                status
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                document_id,
                filename,
                file_path,
                status,
            ),
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()

# get the document from the tablee
def get_document(document_id: str):
    connection = get_mysql_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                document_id,
                filename,
                file_path,
                status,
                created_at
            FROM documents
            WHERE document_id = %s
        """

        cursor.execute(query, (document_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def update_document_status(
    document_id: str,
    status: str,
):
    connection = get_mysql_connection()

    try:
        cursor = connection.cursor()

        query = """
            UPDATE documents
            SET status = %s
            WHERE document_id = %s
        """

        cursor.execute(
            query,
            (status, document_id),
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()

def get_all_documents():
    connection = get_mysql_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                document_id,
                filename,
                status,
                created_at
            FROM documents
            ORDER BY created_at DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()