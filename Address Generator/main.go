package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"

	"github.com/joho/godotenv"
	"github.com/xuri/excelize/v2"
)

var KEY string

type District struct {
	// Level string `json:"level"`
	Name string `json:"name"`
}

type DistrictsResponse struct {
	District
	Districts []District `json:"districts"`
}

type AMapResponse struct {
	Status    string              `json:"status"`
	Districts []DistrictsResponse `json:"districts"`
}

func GetDistricts(keyword string) []string {
	url := "http://restapi.amap.com/v3/config/district?key=" + KEY + "&keywords=" + keyword + "&subdistrict=1&extensions=base"

	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		println("err:", err)
		return nil
	}

	var res AMapResponse
	err = json.Unmarshal(body, &res)
	if err != nil {
		println("err:", err)
		return nil
	}

	districts := make([]string, len(res.Districts[0].Districts))
	// districts[0] = "请选择"
	for i, d := range res.Districts[0].Districts {
		districts[i] = d.Name
	}

	return districts
}

func main() {
	godotenv.Load()
	KEY = os.Getenv("AMAP_KEY")

	f := excelize.NewFile()
	total := 0

	for i, p := range GetDistricts("中国") {
		fmt.Println("Now1:", i, p, total)
		for j, c := range GetDistricts(p) {
			fmt.Println("Now2:", j, c)
			for _, d := range GetDistricts(c) {
				total++
				f.SetCellValue("Sheet1", "A"+strconv.Itoa(total), p)
				f.SetCellValue("Sheet1", "B"+strconv.Itoa(total), c)
				f.SetCellValue("Sheet1", "C"+strconv.Itoa(total), d)
			}
		}
	}

	// Save spreadsheet by the given path.
	if err := f.SaveAs("address.xlsx"); err != nil {
		fmt.Println(err)
	}
}
