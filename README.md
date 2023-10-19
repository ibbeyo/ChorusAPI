# ChorusAPI
ChorusAPI is wrapper for the chorus.fightthe.pw REST API. Available with async usage.

## Basic API Usage 
###### Importing the module:
```python
import chorusapi
```
###### Get Latest Songs:
```python
chorusapi.latest(10)
```
###### Get Total Songs Count:
```python
choursapi.count()
```
###### Get Random Songs:
```python
chorusapi.random()
```
###### Download Song(s):
```python
song = chorusapi.latest()
chorusapi.download(song, savedir='./library')
```
###### Basic Song Search:
```python
chorusapi.search(query='metallica')
```
###### Advanced Song Search:
```python
from chorusapi import DiffultyType, AdvancedSearch

...

adv_search = AdvancedSearch(artist='born of osiris', tier_guitar='gt1', diff_guitar=[DifficultyType.EASY, DifficultyType.EXPERT])
chorus.search(query=adv_search)

```

## Async API Usage
```python
import chorusapi
...

chorus = chorusapi.Async()
await chorus.random()
await chorus.search(query='megadeth')
await chorus.count()
await chorus.latest()
await chorus.download(...)

```