"""Salesforce 取引先・行動 CRUD サンプル"""

from integrations.crm.salesforce.models.account import Account
from integrations.crm.salesforce.models.credentials import SalesforceCredentials
from integrations.crm.salesforce.models.task import Task
from integrations.crm.salesforce.repositories.account import AccountRepository
from integrations.crm.salesforce.repositories.task import TaskRepository


def main() -> None:
    credentials = SalesforceCredentials.from_env()
    repo = AccountRepository(credentials)
    task_repo = TaskRepository(credentials)

    # ------------------------------------------------------------------ #
    # describe（SObject メタデータ取得）
    # ------------------------------------------------------------------ #
    print("=== Account オブジェクトのメタデータ ===")
    meta = repo.describe()
    print(meta)

    # ------------------------------------------------------------------ #
    # describe_specified_fields（フィールドメタデータ取得）
    # ------------------------------------------------------------------ #
    print("\n=== Account フィールドのメタデータ ===")
    fields = repo.describe_specified_fields(["Name", "Industry", "Rating", "Phone"])
    print(fields)

    # ------------------------------------------------------------------ #
    # 一覧取得
    # ------------------------------------------------------------------ #
    print("=== 取引先一覧（最大10件）===")
    accounts = repo.find_all(limit=10)
    for acc in accounts:
        print(f"  {acc.Id}  {acc.Name}")

    # ------------------------------------------------------------------ #
    # 新規作成
    # ------------------------------------------------------------------ #
    print("\n=== 取引先を新規作成 ===")
    new_id = repo.create(
        Account(
            Name="株式会社テスト",
            Phone="03-0000-0000",
            BillingCity="東京",
            BillingState="東京都",
        )
    )
    print(f"  作成された ID: {new_id}")

    # ------------------------------------------------------------------ #
    # ID で取得
    # ------------------------------------------------------------------ #
    print("\n=== 作成した取引先を取得 ===")
    account = repo.find_by_id(new_id)
    print(f"  Name : {account.Name}")
    print(f"  Phone: {account.Phone}")

    # ------------------------------------------------------------------ #
    # 更新
    # ------------------------------------------------------------------ #
    print("\n=== 取引先を更新 ===")
    repo.update(Account(Id=new_id, Phone="03-9999-9999"))
    updated = repo.find_by_id(new_id)
    print(f"  更新後 Phone: {updated.Phone}")

    # ------------------------------------------------------------------ #
    # 名前で検索
    # ------------------------------------------------------------------ #
    print("\n=== 名前で検索 ===")
    results = repo.search_by_name("テスト")
    for acc in results:
        print(f"  {acc.Id}  {acc.Name}")

    # ------------------------------------------------------------------ #
    # 行動（Task）操作
    # ------------------------------------------------------------------ #
    print("\n=== 取引先に行動を登録 ===")
    task_id = task_repo.create(
        Task(
            WhatId=new_id,
            Subject="電話",
            Status="未着手",
            Priority="中",
            ActivityDate="2025-12-31",
            Description="フォローアップの電話",
        )
    )
    print(f"  作成された行動 ID: {task_id}")

    print("\n=== 取引先に紐づく行動を取得 ===")
    tasks = task_repo.find_by_account(new_id)
    for t in tasks:
        print(f"  {t.Id}  {t.Subject}  {t.Status}")

    print("\n=== 行動を更新 ===")
    task_repo.update(Task(Id=task_id, Status="完了"))
    updated_task = task_repo.find_by_id(task_id)
    print(f"  更新後 Status: {updated_task.Status}")

    print("\n=== 行動を削除 ===")
    task_repo.delete(task_id)
    print(f"  ID {task_id} を削除しました")

    # ------------------------------------------------------------------ #
    # 削除
    # ------------------------------------------------------------------ #
    print("\n=== 取引先を削除 ===")
    repo.delete(new_id)
    print(f"  ID {new_id} を削除しました")

    # ------------------------------------------------------------------ #
    # 一括作成
    # ------------------------------------------------------------------ #
    print("\n=== 取引先を一括作成 ===")
    bulk_results = repo.bulk_create(
        [
            Account(Name="株式会社一括テストA"),
            Account(Name="株式会社一括テストB"),
            Account(Name="株式会社一括テストC"),
        ]
    )
    bulk_ids = [r.id for r in bulk_results if r.success]
    for r in bulk_results:
        print(f"  id={r.id}  success={r.success}  errors={r.errors}")

    # ------------------------------------------------------------------ #
    # 一括更新
    # ------------------------------------------------------------------ #
    print("\n=== 取引先を一括更新 ===")
    update_results = repo.bulk_update(
        [
            Account(Id=bulk_ids[0], Phone="03-0001-0001"),
            Account(Id=bulk_ids[1], Phone="03-0002-0002"),
            Account(Id=bulk_ids[2], Phone="03-0003-0003"),
        ]
    )
    for r in update_results:
        print(f"  id={r.id}  success={r.success}")

    # ------------------------------------------------------------------ #
    # 一括削除
    # ------------------------------------------------------------------ #
    # print("\n=== 取引先を一括削除 ===")
    delete_results = repo.bulk_delete(bulk_ids)
    for r in delete_results:
        print(f"  id={r.id}  success={r.success}")


if __name__ == "__main__":
    main()
