fatorial :: Integer -> Integer
fatorial 0 = 1
fatorial n = n * fatorial (n - 1)


main :: IO ()
main = do
    putStrLn "Digita um numero:"
    num <- getLine
    let n = read num :: Integer
    putStrLn ("O fatorial de " ++ show n ++" eh " ++ show(fatorial n))