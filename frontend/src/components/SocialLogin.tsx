import { FaComment, FaGithub } from "react-icons/fa";
import { Box, Button, Divider, HStack, Text, VStack } from "@chakra-ui/react";

const isDebug =
  process.env.REACT_APP_DEBUG === "on" ||
  process.env.REACT_APP_DEBUG === "true";


const redirectUri = isDebug
  ? "http://localhost:3000/social/kakao"
  : "http://airbnb-beta.ggorockee.com/social/kakao";

export default function SocialLogin() {
  const kakaoParams = {
    client_id: "c65ba131d4497c8389e078cfbe59469e",
    redirect_uri: redirectUri,
    response_type: "code",
  };
  const params = new URLSearchParams(kakaoParams).toString();
  return (
    <Box mb={4}>
      <HStack my={8}>
        <Divider />
        <Text textTransform={"uppercase"} color="gray.500" fontSize="xs" as="b">
          Or
        </Text>
        <Divider />
      </HStack>
      <VStack>
        <Button
          as="a"
          href="https://github.com/login/oauth/authorize?client_id=5195598d392601f20eea&scope=read:user,user:email"
          w="100%"
          leftIcon={<FaGithub />}
        >
          Continue with Github
        </Button>
        <Button
          as="a"
          href={`https://kauth.kakao.com/oauth/authorize?${params}`}
          w="100%"
          leftIcon={<FaComment />}
          colorScheme={"yellow"}
        >
          Continue with Kakao
        </Button>
      </VStack>
    </Box>
  );
}