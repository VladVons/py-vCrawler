Host="localhost"
Port="5433"
DbName="crawler_used"
User="crawler_used_user1"
#
File="$(hostname)_${DbName}.sql.dat"
Date=$(date "+%y%m%d-%H%M")
Path=${Host}_${Date}_${File}


Backup()
{
    echo "dump $Path ..."
    pg_dump --verbose --host=$Host --port=$Port --username=$User --dbname=$DbName | zstd > $Path.zst
}

BackupData()
{
    echo "dump $Path ..."
    pg_dump --host=$Host --port=$Port --username=$User --dbname=$DbName --data-only --column-inserts > $Path
}

Restore()
{
    zstd -dc $Path.zst | psql --host=$Host --port=$Port --username=$User --dbname=$DbName
}

VacuumDb()
{
    echo "vacuum $Path ..."
    vacuumdb --verbose --host=$Host --port=$Port --username=$User --dbname=$DbName
}

clear
Backup
#BackupData
#Restore
#VacuumDb
