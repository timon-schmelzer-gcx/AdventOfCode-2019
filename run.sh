for DAY in `ls days`;
do
    echo "Day ${DAY}: " && python "days/${DAY}/solution.py";
done
