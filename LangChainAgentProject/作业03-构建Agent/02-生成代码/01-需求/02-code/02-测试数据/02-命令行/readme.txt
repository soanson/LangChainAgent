

######
我们中的大多数人都需要解析一下命令行参数。
如果我们没有一个方便的工具，那么我们就简单地处理一下传入 main 函数的字符串数组。
有很多开源工具可以完成这个任务，但它们可能并不能完全满足我们的要求。所以我们再写一个吧。

你的任务是实现一个简单的命令行参数解析器。这个解析器应该能够解析字符串数组，这个字符串数组包含了命令行参数。
-l -p 8080 -d /usr/logs  -g this is a list
“l”（日志）没有相关的值，它是一个布尔标志，如果存在则为 true，不存在则为 false。
“p”（端口）有一个整数值，
“d”（目录）有一个字符串值，标志后面如果存在多个值，则该标志表示一个列表。
  "g"(匹配字符串)  表示一个字符串列表[“this”, “is”, “a”, “list”]
如果参数中没有指定某个标志，那么解析器应该指定一个默认值。例如，false 代表布尔值，0 代表数字， "" 代表字符串，[]代表列表。
如果给出的参数与模式不匹配，重要的是给出一个好的错误信息，准确地解释什么是错误的。
确保你的代码是可扩展的，即如何增加新的数值类型是直接和明显的

这个解析器应该能够处理以下情况：
1. 一个标志由一个字符 - 开始，后面跟着一个字母。例如，-l  -p 8080  -d /usr/logs
2. 一个标志可以有一个值，这个值可以是一个整数，一个字符串，或者一个布尔值。例如，-l -p 8080 -d /usr/logs  -g this is a list
3. 一个标志可以有多个值，这些值可以是整数，字符串，或者布尔值。例如，-g this is a list -d 1 2 -3 5
4. 一个标志可以没有值。例如，-l。
5. 如果一个布尔 标志没有值，那么它的值应该是 false。
6. 如果一个整数 标志没有值，那么它的值应该是 0。
7. 如果一个字符串 标志没有值，那么它的值应该是 ""。
8. 如果一个列表 标志没有值，那么它的值应该是 []。

####
参考测试用例：
###

class CommandLineParserTest {
    @Test
    void testParseArgs() {
        // 测试基本的命令行参数解析
        String[] args1 = {"-l", "-p", "8080", "-d", "/usr/logs"};
        Map<String, Object> result1 = CommandLineParser.parseArgs(args1);
        assertEquals(true, result1.get("l"));
        assertEquals(8080, result1.get("p"));
        assertEquals("/usr/logs", result1.get("d"));

        // 测试带有列表的命令行参数解析
        String[] args2 = {"-g", "this", "is", "a", "list", "-d", "1", "2", "-3", "5"};
        Map<String, Object> result2 = CommandLineParser.parseArgs(args2);
        assertEquals(List.of("this", "is", "a", "list"), result2.get("g"));
        assertEquals(List.of(1, 2, -3, 5), result2.get("d"));

        // 测试默认值
        String[] args3 = {};
        Map<String, Object> result3 = CommandLineParser.parseArgs(args3);
        assertEquals(false, result3.get("l"));
        assertEquals(0, result3.get("p"));
        assertEquals("", result3.get("d"));

        // 测试无效参数
        String[] args4 = {"-p", "abc"};
        assertThrows(NumberFormatException.class, () -> CommandLineParser.parseArgs(args4));
        // 添加更多的测试用例，根据需要进行扩展
    }
}

1：提示词

A：完成多个类（n个），对外提供一个方法 CommandLineParser.parseArgs （）

B：完成单元测试，尽可能覆盖多语句

C:通过代码评审

D：检查是否有坏味道， 以及对应重构 

