# Owner: Jackson / Jaymin
# active + archive lists, add, archive, photo endpoints

from backend.db import get_db_connection

# Adds a new item to the active_items table.
def add_item(item_name, description, category, location, date_found, status="Found"):

    # Make sure all required fields have been provided.
    if not all([item_name, description, category, location, date_found]):
        raise ValueError("All item fields are required.")

    # Make sure the status is valid
    if status not in ["Lost", "Found"]:
        raise ValueError("Status must be Lost or Found.")

    # Connect to the Lost and Found database.
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            # SQL command to insert the new item.
            sql = """
                INSERT INTO active_items
                (item_name, description, category, location, date_found, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            # Execute the SQL command using the supplied information.
            cursor.execute(
                sql,
                (item_name, description, category, location, date_found, status)
            )

            # Retrieve the ID assigned to the new item.
            item_id = cursor.lastrowid

            # Record the addition in the item history table.
            history_sql = """
                INSERT INTO item_history
                (item_id, action_type, details)
                VALUES (%s, 'Added', %s)
            """

            cursor.execute(
                history_sql,
                (item_id, f"Added item: {item_name}")
            )

        # Save both database changes.
        connection.commit()

        return item_id

    except Exception:
        # Undo changes if something goes wron.
        connection.rollback()
        raise

    finally:
        # Close the database commection.
        connection.close()


# Retrieves all active items from the database.
def get_active_items():

    # Connect to the Lost and Found database.
    connection = get_db_connection()

    try:
        #Open a cursor to execture SQL commands.
        with connection.cursor() as cursor:

            # Retrieve all active items, newest additions first.
            sql = """
                SELECT *
                FROM active_items
                ORDER BY created_at DESC
            """

            cursor.execute(sql)

            # Retrieve all matching records.
            items = cursor.fetchall()

            return items

    finally:
        # Close the database connection.
        connection.close()


# Retrieve all archived items from the database.
def get_archived_items():

    # Connect to the Lost and Found database.
    connection = get_db_connection()

    try:
        # Open a cursor to exectue SWL commands.
        with connection.cursor() as cursor:

            # Retrieve all archived items, newest additions first.
            sql = """
                SELECT *
                FROM archive_items
                ORDER BY archived_at DESC
            """

            cursor.execute(sql)

            # Retrieve all matching records.
            items = cursor.fetchall()

            return items

    finally:
        # Close the database connection
        connection.close()


# Updates an existing item in the active_items table.
def update_item(item_id, item_name, description, category, location, date_found, status="Found", admin_id=None):

    # Make sure all required fields have been provided.
    if not all([item_name, description, category, location, date_found]):
        raise ValueError("All item fields are required.")

    # Make sure the status is valid.
    if status not in ["Lost", "Found", "Claimed"]:
        raise ValueError("Status must be Lost, Found, or Claimed.")

    # Connect to the Lost and Found database.
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            # Retrieve the item's current information.
            sql = """
                SELECT *
                FROM active_items
                WHERE item_id = %s
            """

            cursor.execute(sql, (item_id,))
            old_item = cursor.fetchone()

            # Check whether the item exists.
            if old_item is None:
                raise ValueError("Item not found.")


            # Store the proposed updated information.
            new_values = {
                "item_name": item_name,
                "description": description,
                "category": category,
                "location": location,
                "date_found": date_found,
                "status": status
            }

            # Store only fields that have actually changed.
            changes = {}

            for field, new_value in new_values.items():

                # Compare the original value with the new value.
                if str(old_item[field]) != str(new_value):
                    changes[field] = (old_item[field], new_value)

            # Check whether any information actually changed.
            if not changes:
                return "No changes were made."

            # Buold the SQL update statement using the changed fields.
            set_clause = ", ".join(
                f"{field} = %s" for field in changes
            )

            # Collect the new values for the SQL statement.
            values = [new_value for old_value, new_value in changes.values()]

            # Add the item ID to identify which record to update.
            values.append(item_id)

            #Update the item in the database.
            sql = f"""
                UPDATE active_items
                SET {set_clause}
                WHERE item_id = %s
            """

            cursor.execute(sql, values)

            # Record each changed field in the item history table.
            for field, (old_value, new_value) in changes.items():

                # Use Claimed as the action type when the status changes to Claimed.
                action_type = "Updated"

                if field == "status" and new_value == "Claimed":
                    action_type = "Claimed"


                history_sql = """
                    INSERT INTO item_history
                    (item_id, admin_id, action_type, changed_field, old_value, new_value, details)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(
                    history_sql,
                    (
                        item_id,
                        admin_id,
                        action_type,
                        field,
                        str(old_value),
                        str(new_value),
                        f"Changed {field} from {old_value} to {new_value}"
                    )
                )

            # Save the item update and history entried together.
            connection.commit()

            return "Item updated successfully."

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()



# Removes an item from the active)items table.
def remove_item(item_id, admin_id=None):

    # COnnect to the Lost and Found database.
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            # Retrieve the item before removing it.
            sql = """
                SELECT *
                FROM active_items
                WHERE item_id = %s
            """

            cursor.execute(sql, (item_id,))
            item = cursor.fetchone()


            # Check whether the item exists.
            if item is None:
                raise ValueError("Item not found.")

            # Record the removal in the item history table.
            history_sql = """
                INSERT INTO item_history
                (item_id, admin_id, action_type, details)
                VALUES (%s, %s, 'Removed', %s)
            """

            cursor.execute(
                history_sql,
                (item_id, admin_id, f"Removed item: {item['item_name']}")
            )

            # Remove the item from the active_items table.
            delete_sql = """
                DELETE FROM active_items
                WHERE item_id = %s
            """

            cursor.execute(delete_sql, (item_id,))

        # Save the history entry and item removal together.
        connection.commit()

        return "Item removed successfully."

    except Exception:
        # Undo changes if something goes wrong.
        connection.rollback()
        raise

    finally:
        # Close the database connection.
        connection.close()


# Marks an existing iem as claimed.
def claim_item(item_id, admin_id=None):

    # Connect to the Lost and Found database.
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            # Retrieve the item's current information.
            sql = """
                SELECT *
                FROM active_items
                WHERE item_id = %s
            """

            cursor.execute(sql, (item_id,))
            item = cursor.fetchone()

            # Check whether the item exists.
            if item is None:
                raise ValueError("Item not found.")

            # Check whether the item has already been claimed.
            if item["status"] == "Claimed":
                raise ValueError("Item has already been claimed.")

            # Update the item's status.
            update_sql = """
                UPDATE active_items
                SET status = 'Claimed'
                WHERE item_id = %s
            """

            cursor.execute(update_sql, (item_id,))

            # Record the claim in the item history table.
            history_sql = """
                INSERT INTO item_history
                (item_id, admin_id, action_type, changed_field, old_value, new_value, details)
                VALUES ( %s, %s, 'Claimed', 'status', %s, 'Claimed', %s)
            """

            cursor.execute(
                history_sql,
                (
                    item_id,
                    admin_id,
                    item["status"],
                    f"Claimed item: {item['item_name']}"
                )
            )

        # Save the status update and history entry together.
        connection.commit()

        return "Item claimed successfully."

    except Exception:
        # Undo changes if something goes wrong.
        connection.rollback()
        raise

    finally:
        # Close the database connection.
        connection.close()